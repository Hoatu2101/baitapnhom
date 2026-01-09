import { useEffect, useState } from "react";
import { View, TouchableOpacity } from "react-native";
import { Chip } from "react-native-paper";
import Apis, { endpoints } from "../utils/Apis";
import MyStyles from "../styles/MyStyles";

const ServiceCategories = ({ setCategory }) => {
  const [categories, setCategories] = useState([]);

  const load = async () => {
    const res = await Apis.get(endpoints.categories);
    setCategories(res.data);
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <View style={MyStyles.row}>
      <TouchableOpacity onPress={() => setCategory(null)}>
        <Chip style={MyStyles.margin}>Tất cả</Chip>
      </TouchableOpacity>

      {categories.map((c) => (
        <TouchableOpacity key={c.id} onPress={() => setCategory(c.id)}>
          <Chip style={MyStyles.margin}>{c.name}</Chip>
        </TouchableOpacity>
      ))}
    </View>
  );
};

export default ServiceCategories;
