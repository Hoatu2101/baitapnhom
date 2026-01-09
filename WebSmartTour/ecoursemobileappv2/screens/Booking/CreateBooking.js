import { View, Text } from "react-native";
import { Button } from "react-native-paper";
import { useContext, useState } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { MyUserContext } from "../../utils/MyContexts";
import { authApis, endpoints } from "../../utils/Apis";
import MyStyles from "../../styles/MyStyles";

const CreateBooking = ({ route, navigation }) => {
  const serviceId = route.params.serviceId;
  const [loading, setLoading] = useState(false);
  const [user] = useContext(MyUserContext);

  const book = async () => {
    try {
      setLoading(true);
      const token = await AsyncStorage.getItem("token");

      await authApis(token).post(endpoints.bookings, {
        service_id: serviceId,
      });

      navigation.navigate("MyBookings");
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return <Text>Bạn cần đăng nhập để đặt dịch vụ</Text>;
  }

  return (
    <View style={MyStyles.padding}>
      <Text style={MyStyles.title}>Xác nhận đặt dịch vụ</Text>
      <Button mode="contained" loading={loading} onPress={book}>
        Đặt ngay
      </Button>
    </View>
  );
};

export default CreateBooking;
