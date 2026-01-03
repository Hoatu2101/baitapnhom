import { StyleSheet } from "react-native";

export default StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: '#fff',
      marginTop: 60
    },
    row: {
        flexDirection: "row",
        flexWrap: 'wrap'
    },
    margin: {
        margin: 5
    },
    padding: {
        padding: 8
    },
    avatar: {
        width: 120,
        height: 120,
        borderRadius: 50
    }, title: {
        fontSize: 30,
        fontWeight: "bold",
        color: "blue",
        alignSelf: "center"
    }
});