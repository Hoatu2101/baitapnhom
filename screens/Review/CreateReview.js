import { Button, TextInput } from "react-native-paper";
import { useState } from "react";
import { authApis, endpoints } from "../../utils/Apis";
import AsyncStorage from "@react-native-async-storage/async-storage";

export default function CreateReview({ route }) {
  const { serviceId } = route.params;
  const [content, setContent] = useState("");
  const [rating, setRating] = useState("");

  const submit = async () => {
    let token = await AsyncStorage.getItem("token");
    try {
      await authApis(token).post("/api/reviews/", {
        service_id: serviceId,
        rating: Number(rating),  
        comment: comment.trim()
      });


      alert("Đánh giá thành công");
    } catch (err) {
      console.log(err);
      alert("Lỗi đánh giá");
    }
  };

  return (
    <>
      <TextInput label="Nội dung" value={content} onChangeText={setContent} />
      <TextInput label="Sao (1-5)" value={rating} onChangeText={setRating} />
      <Button onPress={submit}>Gửi đánh giá</Button>
    </>
  );
}
