import { useEffect, useState, useContext } from "react";
import { ScrollView, Alert } from "react-native";
import { Text, Button, TextInput, Card } from "react-native-paper";
import Apis, { BASE_URL, endpoints, authApis } from "../../utils/Apis";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { MyUserContext } from "../../utils/MyContexts";
import RenderHTML from "react-native-render-html";

export default function ServiceDetails({ route, navigation }) {
  const { serviceId } = route.params;
  const [service, setService] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [canReview, setCanReview] = useState(false);
  const [content, setContent] = useState("");
  const [user] = useContext(MyUserContext);


  // Load service + comment
  useEffect(() => {
    const load = async () => {
      const s = await Apis.get(endpoints.serviceDetails(serviceId));
      setService(s.data);

      const r = await Apis.get(endpoints.reviews(serviceId));
      setReviews(r.data);
    };
    load();
  }, [serviceId]);

  // Realtime comment (polling)
  useEffect(() => {
    const timer = setInterval(async () => {
      const r = await Apis.get(endpoints.reviews(serviceId));
      setReviews(r.data);
    }, 5000);

    return () => clearInterval(timer);
  }, [serviceId]);

  useEffect(() => {
  if (!user) return;

  const checkBooking = async () => {
    try {
      const token = await AsyncStorage.getItem("token");
      const res = await authApis(token).get("/api/bookings/");
      const booked = res.data.some(b => b.service.id === serviceId);
      setCanReview(booked);
    } catch (e) {
      setCanReview(false);
    }
  };

  checkBooking();
}, [user, serviceId]);

  const requireLogin = (callback) => {
    if (!user) {
      Alert.alert(
        "Yêu cầu đăng nhập",
        "Bạn cần đăng nhập để thực hiện chức năng này",
        [
          { text: "Đăng nhập", onPress: () => navigation.navigate("Login") },
          { text: "Hủy", style: "cancel" }
        ]
      );
      return;
    }
    callback();
  };

  const addReview = async () => {
    requireLogin(async () => {
      const token = await AsyncStorage.getItem("token");
      const res = await authApis(token).post("/api/reviews/", {
        service: serviceId,
        content,
      });
      setReviews([res.data, ...reviews]);
      setContent("");
    });
  };

  if (!service) return null;

  return (
    <ScrollView>
      <Card>
        <Card.Cover
          source={{
            uri: service.image
              ? service.image.startsWith("http")
                ? service.image
                : `${BASE_URL}/${service.image}`
              : "https://via.placeholder.com/300",
          }}
        />
        <Card.Content>
          <Text variant="titleLarge">{service.name}</Text>

          {/* Clean HTML description */}
          <RenderHTML
            contentWidth={300}
            source={{ html: service.description }}
          />

          <Text style={{ marginTop: 10 }}>
            Giá: {Number(service.price).toLocaleString()} VNĐ
          </Text>
        </Card.Content>
      </Card>

      {/* ĐẶT DỊCH VỤ – CHẶN KHI CHƯA LOGIN */}
      <Button
        mode="contained"
        style={{ margin: 10 }}
        onPress={() =>
          requireLogin(() =>
            navigation.navigate("CreateBooking", { serviceId })
          )
        }
      >
        Đặt dịch vụ
      </Button>

      {/* COMMENT */}
      <Card style={{ margin: 10 }}>
        <Card.Content>
          <Text variant="titleMedium">Bình luận</Text>

          {user ? (
            <>
              <TextInput
                label="Nhập bình luận"
                value={content}
                onChangeText={setContent}
              />
              <Button onPress={addReview}>Gửi</Button>
            </>
          ) : (
            <Text style={{ marginTop: 10, fontStyle: "italic" }}>
              Đăng nhập để bình luận
            </Text>
          )}

          {reviews.map(r => (
            <Text key={r.id} style={{ marginTop: 5 }}>
              {r.user.username}: {r.content}
            </Text>
          ))}
        </Card.Content>
      </Card>
    </ScrollView>
  );
}
