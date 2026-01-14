import { View, Text, Image, ImageBackground, StyleSheet, Dimensions, KeyboardAvoidingView, Platform, ScrollView } from "react-native";
// import MyStyles from "../../styles/MyStyles"; // Tạm thời comment dòng này để dùng styles mới bên dưới
import { Button, HelperText, TextInput } from "react-native-paper";
import { useContext, useState } from "react";
import { useNavigation } from "@react-navigation/native";
import Apis, { authApis, endpoints } from "../../utils/Apis";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { MyUserContext } from "../../utils/MyContexts";

// Lấy chiều cao màn hình để căn chỉnh
const { height } = Dimensions.get("window");

const Login = ({ route }) => {
    const info = [{
        "label": "Tên đăng nhập",
        "field": "username",
        "icon": "account-outline" // Đổi icon cho hợp bộ icon material
    }, {
        "label": "Mật khẩu",
        "field": "password",
        "icon": "lock-outline",
        "secureTextEntry": true
    }];

    const [user, setUser] = useState({});
    const [errMsg, setErrMsg] = useState();
    const [loading, setLoading] = useState(false);
    const nav = useNavigation();
    const [, dispatch] = useContext(MyUserContext);

    const validate = () => {
        if (!user.username) {
            setErrMsg("Vui lòng nhập tên đăng nhập!");
            return false;
        }
        if (!user.password) {
            setErrMsg("Vui lòng nhập mật khẩu!");
            return false;
        }
        setErrMsg(null);
        return true;
    }

    const login = async () => {
    if (!validate()) return;

    try {
        setLoading(true);

        let res = await Apis.post(endpoints.login, {
            username: user.username,
            password: user.password,
        });

        await AsyncStorage.setItem("token", res.data.access);

        let userRes = await authApis(res.data.access)
            .get(endpoints.currentUser);

        dispatch({
            type: "login",
            payload: userRes.data
        });

        nav.navigate(route.params?.next || "Home");

    } catch (ex) {
        setErrMsg("Tên đăng nhập hoặc mật khẩu không đúng!");
        console.log(ex.response?.data);
    } finally {
        setLoading(false);
    }
};



    return (
        <ImageBackground 
            source={{uri: 'https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?q=80&w=2070&auto=format&fit=crop'}} 
            style={styles.background}
            resizeMode="cover"
        >
            {/* Lớp phủ màu đen mờ để làm nổi bật nội dung */}
            <View style={styles.overlay} />

            <KeyboardAvoidingView 
                behavior={Platform.OS === "ios" ? "padding" : "height"}
                style={styles.container}
            >
                <ScrollView contentContainerStyle={styles.scrollContent}>
                    
                    {/* Phần Header: Logo và Slogan */}
                    <View style={styles.headerContainer}>
                        {/* Thay icon này bằng Logo App của bạn */}
                        <Image 
                            source={{uri: 'https://cdn-icons-png.flaticon.com/512/826/826070.png'}} 
                            style={styles.logo} 
                        />
                        <Text style={styles.appName}>SMART TOUR</Text>
                        <Text style={styles.slogan}>Khám phá thế giới của bạn</Text>
                    </View>

                    {/* Phần Form đăng nhập */}
                    <View style={styles.formContainer}>
                        <Text style={styles.title}>Đăng Nhập</Text>

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
                                activeOutlineColor="#00CEC9" // Màu xanh ngọc (Teal)
                                theme={{ roundness: 15 }}
                                secureTextEntry={i.secureTextEntry}
                                textColor="#333"
                                left={<TextInput.Icon icon={i.icon} color="#666" />}
                                value={user[i.field]}
                                onChangeText={t => setUser({...user, [i.field]: t})} 
                            />
                        ))}

                        <Button 
                            loading={loading} 
                            disabled={loading} 
                            mode="contained" 
                            style={styles.button}
                            contentStyle={styles.buttonContent}
                            labelStyle={styles.buttonLabel}
                            onPress={login}
                        >
                            KHÁM PHÁ NGAY
                        </Button>
                        
                        {/* Link đăng ký / Quên mật khẩu */}
                        <View style={styles.footerAction}>
                            <Text style={styles.footerText}>Chưa có tài khoản? </Text>
                            <Text style={styles.linkText} onPress={() => nav.navigate('Register')}>Đăng ký</Text>
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
        backgroundColor: 'rgba(0,0,0,0.3)', // Làm tối ảnh nền 30%
    },
    container: {
        flex: 1,
    },
    scrollContent: {
        flexGrow: 1,
        justifyContent: 'center',
        padding: 20,
    },
    headerContainer: {
        alignItems: 'center',
        marginBottom: 40,
    },
    logo: {
        width: 80,
        height: 80,
        marginBottom: 10,
        tintColor: '#fff' // Logo màu trắng
    },
    appName: {
        fontSize: 32,
        fontWeight: 'bold',
        color: '#fff',
        letterSpacing: 2,
        textShadowColor: 'rgba(0, 0, 0, 0.75)',
        textShadowOffset: {width: -1, height: 1},
        textShadowRadius: 10
    },
    slogan: {
        color: '#f0f0f0',
        fontSize: 16,
        fontStyle: 'italic',
    },
    formContainer: {
        backgroundColor: 'rgba(255, 255, 255, 0.95)', // Nền trắng mờ
        borderRadius: 25,
        padding: 25,
        shadowColor: "#000",
        shadowOffset: {
            width: 0,
            height: 4,
        },
        shadowOpacity: 0.30,
        shadowRadius: 4.65,
        elevation: 8,
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#2d3436',
        textAlign: 'center',
        marginBottom: 20,
    },
    input: {
        backgroundColor: '#fff',
        marginBottom: 15,
        height: 50,
    },
    errorText: {
        textAlign: 'center',
        fontSize: 14,
        fontWeight: 'bold',
        marginBottom: 10
    },
    button: {
        marginTop: 10,
        backgroundColor: '#00CEC9', // Màu xanh ngọc đặc trưng du lịch
        borderRadius: 25,
        elevation: 5,
    },
    buttonContent: {
        height: 50,
    },
    buttonLabel: {
        fontSize: 16,
        fontWeight: 'bold',
        letterSpacing: 1,
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

export default Login;