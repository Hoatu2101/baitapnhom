
import { View, Text } from "react-native";
import MyStyles from "../../styles/MyStyles";
import { Button } from "react-native-paper";
import { useContext } from "react";
import { MyUserContext } from "../../utils/MyContexts";
import AsyncStorage from "@react-native-async-storage/async-storage";

const Profile = () => {
    const [user, dispatch] = useContext(MyUserContext);

    const logout = async () => {
        await AsyncStorage.removeItem("token");

        dispatch({
            "type": "logout"
        });
    }
    console.info(user);
    return (
        <View>
            <Text style={MyStyles.title}>Chào {user.username}!</Text>

            <Button icon="logout" onPress={logout}>Đăng xuất</Button>
        </View>
    );
}

export default Profile;
