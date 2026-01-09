import React, { useEffect, useState } from "react";
import { View, Text, FlatList, StyleSheet, ActivityIndicator } from "react-native";
import { Button, Card, Chip, Searchbar } from "react-native-paper";
import { useNavigation } from "@react-navigation/native";
import Apis, { endpoints } from "../../utils/Apis";
import MyStyles from "../../styles/MyStyles";

const Home = () => {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const nav = useNavigation();

  const loadServices = async () => {
    try {
      setLoading(true);
      let res = await Apis.get(endpoints["services"](null));
      setServices(res.data.results || res.data);
    } catch (ex) {
      console.error(ex);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadServices();
  }, []);

  const renderItem = ({ item }) => (
    <Card style={styles.card} mode="elevated">
      <Card.Cover source={{ uri: item.image ? item.image : "https://via.placeholder.com/300" }} style={styles.cardImage} />
      <Card.Content style={styles.cardContent}>
        <View style={styles.rowHeader}>
          <Text style={styles.serviceName} numberOfLines={1}>
            {item.name}
          </Text>
          <Chip icon="tag" style={styles.chip}>
            {item.service_type}
          </Chip>
        </View>
        <Text style={styles.price}>
          {new Intl.NumberFormat("vi-VN", {
            style: "currency",
            currency: "VND",
          }).format(item.price)}
        </Text>
        
        <Text style={styles.date}>
          Khởi hành: {new Date(item.start_date).toLocaleDateString("vi-VN")}
        </Text>
      </Card.Content>
      <Card.Actions style={styles.cardAction}>
        <Button
          mode="contained"
          buttonColor="#00CEC9"
          onPress={() =>
            nav.navigate("Booking", { serviceId: item.id, name: item.name })
          }
        >
          ĐẶT NGAY
        </Button>
      </Card.Actions>
    </Card>
  );

  return (
    <View style={MyStyles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Khám phá Tours</Text>
        <Searchbar
          placeholder="Tìm kiếm..."
          onChangeText={setSearchQuery}
          value={searchQuery}
          style={styles.searchBar}
        />
      </View>
      {loading ? (
        <ActivityIndicator size="large" color="#00CEC9" />
      ) : (
        <FlatList
          data={services}
          renderItem={renderItem}
          keyExtractor={(item) => item.id.toString()}
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
    paddingBottom: 10,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#2d3436",
    marginBottom: 10,
  },
  searchBar: {
    backgroundColor: "#f1f2f6",
    elevation: 0,
    height: 45,
  },
  card: {
    marginBottom: 20,
    backgroundColor: "#fff",
    borderRadius: 15,
    overflow: "hidden",
  },
  cardImage: {
    height: 180,
  },
  cardContent: {
    marginTop: 10,
  },
  rowHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 5,
  },
  serviceName: {
    fontSize: 18,
    fontWeight: "bold",
    flex: 1,
    marginRight: 5,
  },
  chip: {
    height: 30,
    backgroundColor: "#81ecec",
  },
  price: {
    fontSize: 18,
    color: "#d63031",
    fontWeight: "bold",
    marginVertical: 5,
  },
  date: {
    color: "#636e72",
    fontSize: 13,
  },
  cardAction: {
    justifyContent: "flex-end",
    paddingHorizontal: 10,
    paddingBottom: 10,
  },
});

export default Home;