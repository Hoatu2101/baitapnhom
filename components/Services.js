import { useEffect, useState } from "react";
import { FlatList, Image, TouchableOpacity, View } from "react-native";
import { List, Searchbar } from "react-native-paper";
import { useNavigation } from "@react-navigation/native";
import Apis, { endpoints } from "../utils/Apis";
import MyStyles from "../styles/MyStyles";

const Services = ({ category }) => {
  const [services, setServices] = useState([]);
  const [q, setQ] = useState("");
  const nav = useNavigation();

  const load = async () => {
    let url = endpoints.services;
    if (q) url += `?q=${q}`;
    if (category) url += `${q ? "&" : "?"}category=${category}`;

    const res = await Apis.get(url);
    setServices(res.data.results || res.data);
  };

  useEffect(() => {
    load();
  }, [q, category]);

  return (
    <View style={MyStyles.padding}>
      <Searchbar placeholder="Tìm dịch vụ..." value={q} onChangeText={setQ} />

      <FlatList
        data={services}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <List.Item
            title={item.name}
            description={`Giá: ${item.price}`}
            left={() => (
              <TouchableOpacity
                onPress={() =>
                  nav.navigate("ServiceDetails", { serviceId: item.id })
                }
              >
                <Image source={{ uri: item.image }} style={MyStyles.avatar} />
              </TouchableOpacity>
            )}
          />
        )}
      />
    </View>
  );
};

export default Services;
