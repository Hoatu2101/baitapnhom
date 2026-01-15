import { View, Alert } from "react-native";
import { Button, Card, Text } from "react-native-paper";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { authApis } from "../../utils/Apis";

const Payment = ({ route, navigation }) => {
  const { bookingId } = route.params;

  const pay = async () => {
    try {
      const token = await AsyncStorage.getItem("token");
      await authApis(token).post("/api/payments/", {
        booking_id: bookingId
      });

      // Alert.alert("Thành công", "Thanh toán thành công!");
      // navigation.navigate("MyBookings");
      Alert.alert("Thành công", "Thanh toán thành công!", [
        {
          text: "OK",
          onPress: () => navigation.reset({
            index: 0,
            routes: [{ name: "MyBookings" }]
          })
        }
      ]);

    } catch (e) {
      Alert.alert("Lỗi", "Thanh toán thất bại");
    }
  };

  return (
    <View style={{ padding: 15 }}>
      <Card>
        <Card.Content>
          <Text variant="titleLarge">Thanh toán</Text>
          <Text>Hình thức: Thanh toán giả lập</Text>
        </Card.Content>
      </Card>

      <Button
        mode="contained"
        style={{ marginTop: 20 }}
        onPress={pay}
      >
        Thanh toán ngay
      </Button>
    </View>
  );
};

export default Payment;
