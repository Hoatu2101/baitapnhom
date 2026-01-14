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

      const safeData = res.data.filter(
        b => b && b.id && b.service
      );

      setBookings(safeData);
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
    if (!item || !item.service) return null;

    const isPaid = !!item.payment; 
    return (
      <Card style={MyStyles.margin}>
        <Card.Content>
          <Text style={{ fontSize: 16, fontWeight: "bold" }}>
            {item.service.name}
          </Text>

          <Text>
            Giá: {item.service.price?.toLocaleString()} VNĐ
          </Text>

          <Text>
            Trạng thái: {isPaid ? "Đã thanh toán" : "Chưa thanh toán"}
          </Text>
        </Card.Content>

        {!isPaid && (
          <Card.Actions>
            <Button
              mode="contained"
              onPress={() =>
                Alert.alert(
                  "Thanh toán",
                  "Vui lòng thanh toán tại màn hình thanh toán",
                  [{ text: "OK" }]
                )
              }
            >
              Chưa thanh toán
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
