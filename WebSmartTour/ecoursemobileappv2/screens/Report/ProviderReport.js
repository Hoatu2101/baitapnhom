import { View, Text } from "react-native";
import { useEffect, useState } from "react";
import Apis, { authApis, endpoints } from "../../utils/Apis";
import AsyncStorage from "@react-native-async-storage/async-storage";
import MyStyles from "../../styles/MyStyles";

const ProviderReport = () => {
  const [data, setData] = useState(null);

  const load = async () => {
    const token = await AsyncStorage.getItem("token");
    const res = await authApis(token).get(endpoints.providerReport);
    setData(res.data);
  };

  useEffect(() => {
    load();
  }, []);

  if (!data) return null;

  return (
    <View style={MyStyles.padding}>
      <Text>Doanh thu: {data.total_revenue}</Text>
      <Text>Số booking: {data.total_bookings}</Text>
    </View>
  );
};

export default ProviderReport;
