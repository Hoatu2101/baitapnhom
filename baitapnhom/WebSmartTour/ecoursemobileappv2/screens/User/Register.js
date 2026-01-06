import { View, Text, TouchableOpacity, Alert, Image } from "react-native";
import MyStyles from "../../styles/MyStyles";
import { Button, HelperText, TextInput } from "react-native-paper";
import { useState } from "react";
import * as ImagePicker from 'expo-image-picker';
import Apis, { endpoints } from "../../utils/Apis";
import { useNavigation } from "@react-navigation/native";

const Register = () => {
    const info = [{
        "label": "Tên",
        "field": "first_name",
        "icon": "text"
    }, {
        "label": "Họ và tên lót",
        "field": "last_name",
        "icon": "text"
    }, {
        "label": "Tên đăng nhập",
        "field": "username",
        "icon": "account"
    }, {
        "label": "Mật khẩu",
        "field": "password",
        "icon": "eye",
        "secureTextEntry": true
    }, {
        "label": "Xác nhận mật khẩu",
        "field": "confirm",
        "icon": "eye",
        "secureTextEntry": true
    }];

    const [user, setUser] = useState({});
    const [errMsg, setErrMsg] = useState();
    const [loading, setLoading] = useState(false);
    const nav = useNavigation();

    const picker = async () => {
        const {granted} = await ImagePicker.requestMediaLibraryPermissionsAsync();
        if (granted) {
            const res = await ImagePicker.launchImageLibraryAsync();
            if (!res.canceled)
                setUser({...user, "avatar": res.assets[0]});
        } else
            Alert.alert("Permission denied!");
    }

    const validate = () => {
        if (!user.password || !user.confirm || user.password !== user.confirm) {
            setErrMsg("Mật khẩu KHÔNG khớp!");
            return false;
        }

        setErrMsg(null);

        return true;
    }

    const register = async () => {
        if (validate()) {
            try {
                setLoading(true);
                let form = new FormData();
            
                for (let key in user) {
                    if (key !== 'confirm') {
                        if (key === 'avatar') {
                            form.append(key, {
                                uri: user.avatar.uri,
                                name: user.avatar.fileName,
                                type: "image/jpeg" //user.avatar.type
                            });
                        } else
                            form.append(key, user[key]);
                    }
                }

                console.info(form);
    
                let res = await Apis.post(endpoints['register'], form, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
    
                if (res.status === 201) 
                    nav.navigate('Login');
                else
                    setErrMsg("Đã có lỗi xảy ra. Vui lòng thử lại sau!");
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
            <Text style={MyStyles.title}>ĐĂNG KÝ NGƯỜI DÙNG</Text>

            <HelperText type="error" visible={errMsg}>
                {errMsg}
            </HelperText>

            {info.map(i => <TextInput key={i.field} style={MyStyles.margin}
                            label={i.label}
                            secureTextEntry={i.secureTextEntry}
                            right={<TextInput.Icon icon={i.icon} />}
                            value={user[i.field]}
                            onChangeText={t => setUser({...user, [i.field]: t})} />)}

            <TouchableOpacity style={MyStyles.margin} onPress={picker}>
            <Text>Chọn ảnh đại diện...</Text>
            </TouchableOpacity>    

            {user.avatar && <Image  source={{uri: user.avatar.uri}} width={250} style={[MyStyles.avatar, MyStyles.margin]} />}

            <Button loading={loading} disabled={loading} mode="contained" icon="account" onPress={register}>Đăng ký</Button>

        </View>
    );
}

export default Register;