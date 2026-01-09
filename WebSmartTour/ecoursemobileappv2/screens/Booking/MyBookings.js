import { View, Text, FlatList } from "react-native";
import { Button, Card } from "react-native-paper";
import { useEffect, useState } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { authApis, endpoints } from "../../utils/Apis";
import MyStyles from "../../styles/MyStyles";

const MyBookings = () => {
  const [bookings, setBookings] = useState([]);

  const load = async () => {
    const token = await AsyncStorage.getItem("token");
    const res = await authApis(token).get(endpoints.myBookings);
    setBookings(res.data);
  };

  const pay = async (id) => {
    const token = await AsyncStorage.getItem("token");
    await authApis(token).post(endpoints.payments, { booking: id });
    load();
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <FlatList
      data={bookings}
      keyExtractor={(i) => i.id.toString()}
      renderItem={({ item }) => (
        <Card style={MyStyles.margin}>
          <Card.Content>
            <Text>{item.service.name}</Text>
            <Text>Trạng thái: {item.status}</Text>
          </Card.Content>
          {!item.is_paid && (
            <Card.Actions>
              <Button onPress={() => pay(item.id)}>Thanh toán</Button>
            </Card.Actions>
          )}
        </Card>
      )}
    />
  );
};

export default MyBookings;
