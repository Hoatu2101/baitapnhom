import { NavigationContainer } from "@react-navigation/native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { Icon } from "react-native-paper";
import { useReducer } from "react";

import Home from "./screens/Home/Home";
import Services from "./screens/Home/Services";
import ServiceDetails from "./screens/Home/ServiceDetails";

import Login from "./screens/User/Login";
import Register from "./screens/User/Register";
import Profile from "./screens/User/User";

import CreateBooking from "./screens/Booking/CreateBooking";
import MyBookings from "./screens/Booking/MyBookings";

import ProviderReport from "./screens/Report/ProviderReport";
import AdminDashboard from "./screens/Report/AdminDashboard";

import { MyUserContext } from "./utils/MyContexts";
import MyUserReducer from "./reducers/MyUserReducer";

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

const HomeStack = () => (
  <Stack.Navigator>
    <Stack.Screen name="HomeMain" component={Home} options={{ title: "Dịch vụ" }} />
    <Stack.Screen name="ServiceDetails" component={ServiceDetails} options={{ title: "Chi tiết dịch vụ" }} />
    <Stack.Screen name="CreateBooking" component={CreateBooking} options={{ title: "Đặt dịch vụ" }} />
  </Stack.Navigator>
);

const App = () => {
  const [user, dispatch] = useReducer(MyUserReducer, null);

  return (
    <MyUserContext.Provider value={[user, dispatch]}>
      <NavigationContainer>
        <Tab.Navigator screenOptions={{ headerShown: false }}>
          <Tab.Screen
            name="Home"
            component={HomeStack}
            options={{
              tabBarIcon: () => <Icon source="home" size={25} />,
              title: "Trang chủ",
            }}
          />

          {user === null ? (
            <>
              <Tab.Screen
                name="Login"
                component={Login}
                options={{
                  tabBarIcon: () => <Icon source="login" size={25} />,
                  title: "Đăng nhập",
                }}
              />
              <Tab.Screen
                name="Register"
                component={Register}
                options={{
                  tabBarIcon: () => <Icon source="account-plus" size={25} />,
                  title: "Đăng ký",
                }}
              />
            </>
          ) : (
            <>
              <Tab.Screen
                name="MyBookings"
                component={MyBookings}
                options={{
                  tabBarIcon: () => <Icon source="clipboard-list" size={25} />,
                  title: "Đơn đặt",
                }}
              />

              {user.role === "PROVIDER" && (
                <Tab.Screen
                  name="ProviderReport"
                  component={ProviderReport}
                  options={{
                    tabBarIcon: () => <Icon source="chart-bar" size={25} />,
                    title: "Báo cáo",
                  }}
                />
              )}

              {user.is_staff && (
                <Tab.Screen
                  name="AdminDashboard"
                  component={AdminDashboard}
                  options={{
                    tabBarIcon: () => <Icon source="view-dashboard" size={25} />,
                    title: "Quản trị",
                  }}
                />
              )}

              <Tab.Screen
                name="Profile"
                component={Profile}
                options={{
                  tabBarIcon: () => <Icon source="account" size={25} />,
                  title: "Tài khoản",
                }}
              />
            </>
          )}
        </Tab.Navigator>
      </NavigationContainer>
    </MyUserContext.Provider>
  );
}

export default App;
