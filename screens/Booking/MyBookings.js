import { View, Text, FlatList, Alert } from "react-native";
import { Button, Card } from "react-native-paper";
import { useEffect, useState } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { authApis, endpoints } from "../../utils/Apis";
import MyStyles from "../../styles/MyStyles";

const MyBookings = () => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(false);

  const load = async () => {
    try {
      setLoading(true);
      const token = await AsyncStorage.getItem("token");
      const res = await authApis(token).get(endpoints.myBookings);

      setBookings(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      Alert.alert("Lỗi", "Không tải được danh sách đơn đặt");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const renderItem = ({ item }) => {
  const serviceName = item.service?.name ?? "Dịch vụ";
  const price = Number(item.service?.price ?? 0);
  const isPaid = item.payment?.is_paid === true;

  return (
    <Card style={MyStyles.margin}>
      <Card.Content>
        <Text style={{ fontSize: 16, fontWeight: "bold" }}>
          {serviceName}
        </Text>

        <Text>Giá: {price.toLocaleString()} VNĐ</Text>

        <Text>
          Trạng thái: {isPaid ? "Đã thanh toán" : "Chưa thanh toán"}
        </Text>
      </Card.Content>

      {!isPaid && (
        <Card.Actions>
          <Button onPress={() =>
            navigation.navigate("Payment", { bookingId: item.id })
          }>
            Thanh toán
          </Button>
        </Card.Actions>
      )}
    </Card>
  );
};



  return (
    <FlatList
      data={bookings}
      refreshing={loading}
      onRefresh={load}
      keyExtractor={(item) => String(item.id)}
      renderItem={renderItem}
      ListEmptyComponent={
        <View style={{ padding: 20 }}>
          <Text>Bạn chưa có đơn đặt nào</Text>
        </View>
      }
    />
  );
};

export default MyBookings;
