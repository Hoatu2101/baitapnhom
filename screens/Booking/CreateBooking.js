// import { useEffect, useState, useContext } from "react";
// import { ScrollView, Alert } from "react-native";
// import { Card, Button, Text, TextInput } from "react-native-paper";
// import AsyncStorage from "@react-native-async-storage/async-storage";
// import Apis, { authApis, endpoints } from "../../utils/Apis";
// import { MyUserContext } from "../../utils/MyContexts";

// export default function CreateBooking({ route, navigation }) {
//   const { serviceId } = route.params;
//   const [service, setService] = useState(null);
//   const [note, setNote] = useState("");
//   const [user] = useContext(MyUserContext);

//   useEffect(() => {
//     if (!user) {
//       Alert.alert(
//         "Yêu cầu đăng nhập",
//         "Bạn cần đăng nhập để đặt dịch vụ",
//         [
//           { text: "Đăng nhập", onPress: () => navigation.navigate("Login") },
//           { text: "Quay lại", onPress: () => navigation.goBack() }
//         ]
//       );
//       return;
//     }

//     Apis.get(endpoints.serviceDetails(serviceId))
//       .then(res => setService(res.data));
//   }, [serviceId, user]);

//   const createBooking = async () => {
//     const token = await AsyncStorage.getItem("token");

//     const res = await authApis(token).post("/api/bookings/", {
//       service: serviceId,
//       description: note,
//       booking_date: new Date().toISOString(),
//     });

//     navigation.replace("Payment", {
//       booking: res.data,
//       service,
//     });
//   };

//   if (!service) return null;

//   return (
//     <ScrollView>
//       <Card style={{ margin: 10 }}>
//         <Card.Content>
//           <Text variant="titleLarge">{service.name}</Text>
//           <Text>Giá: {service.price} VNĐ</Text>

//           <TextInput
//             label="Ghi chú"
//             value={note}
//             onChangeText={setNote}
//             multiline
//           />

//           <Button mode="contained" onPress={createBooking}>
//             Xác nhận đặt dịch vụ
//           </Button>
//         </Card.Content>
//       </Card>
//     </ScrollView>
//   );
// }


import { View, Alert } from "react-native";
import { Button, Card, Text } from "react-native-paper";
import { useContext } from "react";
import { MyUserContext } from "../../utils/MyContexts";
import { authApis } from "../../utils/Apis";
import AsyncStorage from "@react-native-async-storage/async-storage";

const CreateBooking = ({ route, navigation }) => {
  const { serviceId } = route.params;
  const [user] = useContext(MyUserContext);

  const confirmBooking = async () => {
    if (!user) {
      Alert.alert(
        "Chưa đăng nhập",
        "Bạn cần đăng nhập để đặt dịch vụ",
        [
          { text: "Hủy" },
          { text: "Đăng nhập", onPress: () => navigation.navigate("Login") }
        ]
      );
      return;
    }

    try {
      const token = await AsyncStorage.getItem("token");

      const payload = {
        service_id: serviceId,
        booking_date: new Date().toISOString().split("T")[0] // YYYY-MM-DD
      };

      const res = await authApis(token).post("/api/bookings/", payload);

      navigation.navigate("Payment", {
        bookingId: res.data.id
      });
    } catch (err) {
      console.log("BOOKING ERROR:", err.response?.data);
      Alert.alert("Lỗi", "Không thể đặt dịch vụ");
    }
  };

  return (
    <View style={{ padding: 15 }}>
      <Card>
        <Card.Content>
          <Text variant="titleLarge">Xác nhận đặt dịch vụ</Text>
          <Text>Bạn có chắc chắn muốn đặt dịch vụ này?</Text>
        </Card.Content>
      </Card>

      <Button
        mode="contained"
        style={{ marginTop: 20 }}
        onPress={confirmBooking}
      >
        Xác nhận đặt dịch vụ
      </Button>
    </View>
  );
};

export default CreateBooking;
