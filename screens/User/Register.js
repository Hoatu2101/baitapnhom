import { View, Text, TouchableOpacity, Image, ImageBackground, StyleSheet, Dimensions, KeyboardAvoidingView, Platform, ScrollView } from "react-native";
// import MyStyles from "../../styles/MyStyles"; // Tạm ẩn style cũ
import { Button, HelperText, TextInput, Avatar } from "react-native-paper";
import { useState } from "react";
import * as ImagePicker from 'expo-image-picker';
import Apis, { endpoints } from "../../utils/Apis";
import { useNavigation } from "@react-navigation/native";

const Register = () => {
    const info = [{
        "label": "Tên",
        "field": "first_name",
        "icon": "card-account-details-outline"
    }, {
        "label": "Họ và tên lót",
        "field": "last_name",
        "icon": "card-account-details-outline"
    }, {
        "label": "Tên đăng nhập",
        "field": "username",
        "icon": "account-circle-outline"
    }, {
        "label": "Mật khẩu",
        "field": "password",
        "icon": "lock-outline",
        "secureTextEntry": true
    }, {
        "label": "Xác nhận mật khẩu",
        "field": "confirm",
        "icon": "lock-check-outline",
        "secureTextEntry": true
    }];

    const [user, setUser] = useState({});
    const [errMsg, setErrMsg] = useState();
    const [loading, setLoading] = useState(false);
    const nav = useNavigation();

    const picker = async () => {
        const { granted } = await ImagePicker.requestMediaLibraryPermissionsAsync();
        if (granted) {
            const res = await ImagePicker.launchImageLibraryAsync();
            if (!res.canceled)
                setUser({ ...user, "avatar": res.assets[0] });
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
        if (!validate()) return;

        try {
            setLoading(true);

            let form = new FormData();

            form.append("username", user.username);
            form.append("password", user.password);
            form.append("first_name", user.first_name || "");
            form.append("last_name", user.last_name || "");
            form.append("email", `${user.username}@gmail.com`);

            if (user.avatar) {
            form.append("avatar", {
                uri: user.avatar.uri,
                name: "avatar.jpg",
                type: "image/jpeg",
            });
            }

            const res = await Apis.post(
            endpoints.register,
            form,
            {
                headers: {
                "Content-Type": "multipart/form-data",
                },
            }
            );

            if (res.status === 201) {
            nav.navigate("Login");
            }
        } catch (ex) {
            console.log("REGISTER ERROR:", ex.response?.data || ex.message);
            setErrMsg("Đăng ký thất bại hoặc tài khoản đã tồn tại!");
        } finally {
            setLoading(false);
        }
    };



    return (
        <ImageBackground
            source={{ uri: 'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?q=80&w=2021&auto=format&fit=crop' }} // Hình du lịch (Road trip)
            style={styles.background}
            resizeMode="cover"
        >
            <View style={styles.overlay} />

            <KeyboardAvoidingView
                behavior={Platform.OS === "ios" ? "padding" : "height"}
                style={styles.container}
            >
                <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
                    
                    <View style={styles.headerContainer}>
                        <Text style={styles.title}>ĐĂNG KÝ THÀNH VIÊN</Text>
                        <Text style={styles.subTitle}>Bắt đầu hành trình của bạn ngay hôm nay</Text>
                    </View>

                    <View style={styles.formContainer}>
                        
                        {/* Khu vực chọn Avatar đẹp mắt hơn */}
                        <View style={styles.avatarContainer}>
                            <TouchableOpacity onPress={picker}>
                                {user.avatar ? (
                                    <Image source={{ uri: user.avatar.uri }} style={styles.avatarImage} />
                                ) : (
                                    <View style={styles.avatarPlaceholder}>
                                        <Text style={styles.avatarText}>Ảnh đại diện</Text>
                                        <Text style={styles.avatarIcon}>+</Text>
                                    </View>
                                )}
                            </TouchableOpacity>
                        </View>

                        <HelperText type="error" visible={!!errMsg} style={styles.errorText}>
                            {errMsg}
                        </HelperText>

                        {info.map(i => (
                            <TextInput
                                key={i.field}
                                style={styles.input}
                                label={i.label}
                                mode="outlined"
                                outlineColor="transparent"
                                activeOutlineColor="#00CEC9"
                                theme={{ roundness: 15 }}
                                secureTextEntry={i.secureTextEntry}
                                textColor="#333"
                                left={<TextInput.Icon icon={i.icon} color="#666" />}
                                value={user[i.field]}
                                onChangeText={t => setUser({ ...user, [i.field]: t })}
                            />
                        ))}

                        <Button
                            loading={loading}
                            disabled={loading}
                            mode="contained"
                            style={styles.button}
                            contentStyle={styles.buttonContent}
                            labelStyle={styles.buttonLabel}
                            onPress={register}
                        >
                            ĐĂNG KÝ
                        </Button>

                        <View style={styles.footerAction}>
                            <Text style={styles.footerText}>Đã có tài khoản? </Text>
                            <Text style={styles.linkText} onPress={() => nav.navigate('Login')}>Đăng nhập</Text>
                        </View>
                    </View>
                </ScrollView>
            </KeyboardAvoidingView>
        </ImageBackground>
    );
}

const styles = StyleSheet.create({
    background: {
        flex: 1,
        width: '100%',
        height: '100%',
    },
    overlay: {
        ...StyleSheet.absoluteFillObject,
        backgroundColor: 'rgba(0,0,0,0.5)', // Tối hơn chút để dễ đọc form dài
    },
    container: {
        flex: 1,
    },
    scrollContent: {
        flexGrow: 1,
        justifyContent: 'center',
        padding: 20,
        paddingTop: 60,
        paddingBottom: 40
    },
    headerContainer: {
        alignItems: 'center',
        marginBottom: 20,
    },
    title: {
        fontSize: 28,
        fontWeight: 'bold',
        color: '#fff',
        textTransform: 'uppercase',
        letterSpacing: 1,
        textAlign: 'center'
    },
    subTitle: {
        color: '#f0f0f0',
        fontSize: 14,
        marginTop: 5,
    },
    formContainer: {
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderRadius: 25,
        padding: 20,
        elevation: 10,
    },
    // Style cho Avatar
    avatarContainer: {
        alignItems: 'center',
        marginBottom: 20,
        marginTop: -50, // Đẩy lên trên mép form tạo điểm nhấn
    },
    avatarPlaceholder: {
        width: 100,
        height: 100,
        backgroundColor: '#e1e1e1',
        borderRadius: 50,
        justifyContent: 'center',
        alignItems: 'center',
        borderWidth: 4,
        borderColor: '#fff',
        elevation: 5,
    },
    avatarImage: {
        width: 100,
        height: 100,
        borderRadius: 50,
        borderWidth: 4,
        borderColor: '#fff',
    },
    avatarText: {
        fontSize: 10,
        color: '#666',
        fontWeight: 'bold'
    },
    avatarIcon: {
        fontSize: 30,
        color: '#00CEC9',
        fontWeight: 'bold',
        marginTop: -5
    },
    // Kết thúc style Avatar
    input: {
        backgroundColor: '#fff',
        marginBottom: 12,
        height: 50,
    },
    errorText: {
        textAlign: 'center',
        color: 'red',
        fontWeight: 'bold',
    },
    button: {
        marginTop: 15,
        backgroundColor: '#00CEC9',
        borderRadius: 25,
        elevation: 3,
    },
    buttonContent: {
        height: 50,
    },
    buttonLabel: {
        fontSize: 16,
        fontWeight: 'bold',
        color: '#fff'
    },
    footerAction: {
        flexDirection: 'row',
        justifyContent: 'center',
        marginTop: 20,
    },
    footerText: {
        color: '#636e72',
    },
    linkText: {
        color: '#00CEC9',
        fontWeight: 'bold',
    },
});

export default Register;