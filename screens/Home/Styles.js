import { StyleSheet } from "react-native";
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F5F7FA",
  },
  headerContainer: {
      backgroundColor: '#00CEC9',
      paddingBottom: 15,
      paddingTop: 10,
      paddingHorizontal: 15,
      borderBottomLeftRadius: 20,
      borderBottomRightRadius: 20,
  },
  searchBar: {
    backgroundColor: "#fff",
    borderRadius: 10,
    elevation: 4,
  },
  listContent: {
    padding: 15,
    paddingBottom: 80,
  },
  emptyText: {
      textAlign: 'center',
      marginTop: 30,
      color: '#999'
  },

  card: {
    backgroundColor: "#fff",
    borderRadius: 15,
    marginBottom: 20,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 6,
    elevation: 3,
    overflow: 'hidden',
  },
  cardImage: {
    width: "100%",
    height: 160,
    resizeMode: "cover",
  },
  cardBody: {
      padding: 15,
  },
  headerRow: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'flex-start',
      marginBottom: 10,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#333",
    flex: 1,
    marginRight: 10,
  },
  typeBadge: {
      backgroundColor: '#E0F7FA',
      paddingHorizontal: 8,
      paddingVertical: 4,
      borderRadius: 6,
  },
  typeText: {
      color: '#0097A7',
      fontSize: 10,
      fontWeight: 'bold',
  },
  infoRow: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: 10,
  },
  price: {
    fontSize: 16,
    fontWeight: "bold",
    color: "#00CEC9",
  },
  date: {
      fontSize: 12,
      color: '#666',
  },
  divider: {
      height: 1,
      backgroundColor: '#EEE',
      marginBottom: 10,
  },
  actionRow: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
  },
  detailBtn: {
      padding: 10,
  },
  detailBtnText: {
      color: '#666',
      fontWeight: '600',
  },
  bookBtn: {
      backgroundColor: '#00CEC9',
      borderRadius: 20,
  }
});
export default HomeStyles;