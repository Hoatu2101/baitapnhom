import { View, Text, ScrollView } from "react-native";
import { useContext, useEffect, useState } from "react";
import { Button, Card, TextInput } from "react-native-paper";
import Apis, { authApis, endpoints } from "../../utils/Apis";
import MyStyles from "../../styles/MyStyles";
import { MyUserContext } from "../../utils/MyContexts";
import AsyncStorage from "@react-native-async-storage/async-storage";

const ServiceDetails = ({ route }) => {
  const serviceId = route.params.serviceId;
  const [service, setService] = useState(null);
  const [content, setContent] = useState("");
  const [reviews, setReviews] = useState([]);
  const [user] = useContext(MyUserContext);

  const load = async () => {
    const res = await Apis.get(endpoints.serviceDetails(serviceId));
    setService(res.data);

    const r = await Apis.get(endpoints.reviews(serviceId));
    setReviews(r.data);
  };

  const addReview = async () => {
    const token = await AsyncStorage.getItem("token");
    const res = await authApis(token).post(
      endpoints.reviews(serviceId),
      { content }
    );
    setReviews([res.data, ...reviews]);
    setContent("");
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <ScrollView>
      {service && (
        <Card>
          <Card.Cover source={{ uri: service.image }} />
          <Card.Content>
            <Text style={MyStyles.title}>{service.name}</Text>
            <Text>{service.description}</Text>
            <Text>Giá: {service.price}</Text>
          </Card.Content>
        </Card>
      )}

      {user && (
        <View style={MyStyles.padding}>
          <TextInput
            placeholder="Đánh giá..."
            value={content}
            onChangeText={setContent}
          />
          <Button onPress={addReview}>Gửi đánh giá</Button>
        </View>
      )}

      {reviews.map((r) => (
        <Text key={r.id} style={MyStyles.margin}>
          {r.user.username}: {r.content}
        </Text>
      ))}
    </ScrollView>
  );
};

export default ServiceDetails;
