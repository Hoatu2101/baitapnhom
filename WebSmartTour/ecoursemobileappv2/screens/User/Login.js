import { View, Text, Image } from "react-native";
import MyStyles from "../../styles/MyStyles";
import { Button, HelperText, TextInput } from "react-native-paper";
import { useContext, useState } from "react";
import { useNavigation } from "@react-navigation/native";
import Apis, { authApis, endpoints } from "../../utils/Apis";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { MyUserContext } from "../../utils/MyContexts";

const Login = () => {
    const info = [{
        "label": "Tên đăng nhập",
        "field": "username",
        "icon": "account"
    }, {
        "label": "Mật khẩu",
        "field": "password",
        "icon": "eye",
        "secureTextEntry": true
    }];

    const [user, setUser] = useState({});
    const [errMsg, setErrMsg] = useState();
    const [loading, setLoading] = useState(false);
    // const nav = useNavigation();
    const [,dispatch] = useContext(MyUserContext);

    const validate = () => {
        if (!user.username) {
            setErrMsg("Vui lòng nhập username!");
            return false;
        }
        if (!user.password) {
            setErrMsg("Vui lòng nhập password!");
            return false;
        }

        setErrMsg(null);

        return true;
    }

    const login = async () => {
        if (validate()) {
            try {
                setLoading(true);
                
                let res = await Apis.post(endpoints['login'], {
                    ...user,
                    'client_id': '4jr0cMT5CiZAW3ZAaW5Sx3Ex9JC1yNjnK34k85ga', // lưu vào biến môi trường react
                    'client_secret': '2gYKjItC9dWyLTpzodprh8P3Pk8TUgkyOuSB1JmVMH3wW6s3e4HgvIw9QGkY7M2w5xLNY1TxMB3pWxPYv0MkmBOMAlYM9PKrPwYdZ9SBEgEZrbg3gbctt5LF965qMNEh',
                    'grant_type': 'password'
                });
                console.info(res.data);
                await AsyncStorage.setItem("token", res.data.access_token);

                setTimeout(async () => {
                    let user = await authApis(res.data.access_token).get(endpoints['current-user']);
                    console.info(user.data);

                    dispatch({
                        "type": "login",
                        "payload": user.data
                    });
                }, 500);
                
            } catch (ex) {
                setErrMsg("Đã có lỗi xảy ra. Vui lòng thử lại sau!");
                console.info(ex);
            } finally {
                setLoading(false);
            }
        }
    }

    return (
        <View style={MyStyles.padding}>
            <Text style={MyStyles.title}>ĐĂNG NHẬP NGƯỜI DÙNG</Text>

            <HelperText type="error" visible={errMsg}>
                {errMsg}
            </HelperText>

            {info.map(i => <TextInput key={i.field} style={MyStyles.margin}
                            label={i.label}
                            secureTextEntry={i.secureTextEntry}
                            right={<TextInput.Icon icon={i.icon} />}
                            value={user[i.field]}
                            onChangeText={t => setUser({...user, [i.field]: t})} />)}

          
            {user.avatar && <Image  source={{uri: user.avatar.uri}} width={250} style={[MyStyles.avatar, MyStyles.margin]} />}

            <Button loading={loading} disabled={loading} mode="contained" icon="account" onPress={login}>Đăng nhập</Button>

        </View>
    );
}

export default Login;