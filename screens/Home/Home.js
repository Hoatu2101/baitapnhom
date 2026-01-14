import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  FlatList,
  ActivityIndicator,
  Image,
  TouchableOpacity,
  StyleSheet,
} from "react-native";
import { Card, Searchbar } from "react-native-paper";
import { useNavigation } from "@react-navigation/native";
import Apis from "../../utils/Apis";
import MyStyles from "../../styles/MyStyles";

const PAGE_SIZE = 20;

const Home = () => {
  const [allServices, setAllServices] = useState([]);
  const [services, setServices] = useState([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const navigation = useNavigation();

  const loadServices = async () => {
    try {
      setLoading(true);
      const res = await Apis.get("/api/services/");
      setAllServices(res.data);
      setServices(res.data.slice(0, PAGE_SIZE));
      setPage(1);
    } catch (err) {
      console.error("Load services error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadServices();
  }, []);

  const loadMore = () => {
    const nextPage = page + 1;
    const start = page * PAGE_SIZE;
    const end = nextPage * PAGE_SIZE;

    const more = allServices.slice(start, end);
    if (more.length > 0) {
      setServices((prev) => [...prev, ...more]);
      setPage(nextPage);
    }
  };

  const filteredServices = services.filter((s) =>
    s.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const renderItem = ({ item }) => {
    const imageUrl = item.image
      ? item.image
      : "https://via.placeholder.com/300";

    return (
      <Card style={styles.card}>
        <TouchableOpacity
          onPress={() =>
            navigation.navigate("ServiceDetails", {
              serviceId: item.id,
            })
          }
        >
          <Image
            source={{ uri: imageUrl }}
            style={styles.cardImage}
            resizeMode="cover"
          />
        </TouchableOpacity>

        <Card.Content>
          <Text style={styles.serviceName}>{item.name}</Text>
          <Text style={styles.price}>
            {Number(item.price).toLocaleString("vi-VN")} VNĐ
          </Text>
        </Card.Content>
      </Card>
    );
  };

  return (
    <View style={MyStyles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Khám phá dịch vụ</Text>
        <Searchbar
          placeholder="Tìm kiếm..."
          value={searchQuery}
          onChangeText={setSearchQuery}
          style={styles.searchBar}
        />
      </View>

      {loading ? (
        <ActivityIndicator size="large" color="#00CEC9" />
      ) : (
        <FlatList
          data={filteredServices}
          renderItem={renderItem}
          keyExtractor={(item) => item.id.toString()}
          onEndReached={loadMore}
          onEndReachedThreshold={0.7}
          contentContainerStyle={{ padding: 10, paddingBottom: 80 }}
        />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  header: {
    padding: 15,
    backgroundColor: "#fff",
    paddingTop: 40,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 10,
  },
  searchBar: {
    backgroundColor: "#f1f2f6",
    height: 45,
  },
  card: {
    marginBottom: 20,
    borderRadius: 15,
    overflow: "hidden",
  },
  cardImage: {
    height: 180,
    width: "100%",
  },
  serviceName: {
    fontSize: 18,
    fontWeight: "bold",
    marginTop: 8,
  },
  price: {
    fontSize: 16,
    color: "#d63031",
    marginVertical: 5,
  },
});

export default Home;
