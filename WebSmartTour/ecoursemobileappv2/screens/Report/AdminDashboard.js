import { View, Text } from "react-native";
import { useEffect, useState } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { authApis, endpoints } from "../../utils/Apis";
import MyStyles from "../../styles/MyStyles";

const AdminDashboard = () => {
  const [data, setData] = useState(null);

  const load = async () => {
    const token = await AsyncStorage.getItem("token");
    const res = await authApis(token).get(endpoints.adminReport);
    setData(res.data);
  };

  useEffect(() => {
    load();
  }, []);

  if (!data) return null;

  return (
    <View style={MyStyles.padding}>
      <Text style={MyStyles.title}>BÁO CÁO HỆ THỐNG</Text>
      <Text>Tổng dịch vụ: {data.total_services}</Text>
      <Text>Tổng booking: {data.total_bookings}</Text>
      <Text>Tổng doanh thu: {data.total_revenue}</Text>
    </View>
  );
};

export default AdminDashboard;
