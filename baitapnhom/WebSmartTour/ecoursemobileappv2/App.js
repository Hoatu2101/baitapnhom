
import Home from "./screens/Home/Home";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import Lessons from "./screens/Home/Lessons";
import { NavigationContainer } from "@react-navigation/native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import Register from "./screens/User/Register";
import Login from "./screens/User/Login";
import { Icon } from "react-native-paper";
import { MyUserContext } from "./utils/MyContexts";
import { useContext, useReducer } from "react";
import MyUserReducer from "./reducers/MyUserReducer";
import Profile from "./screens/User/User";

const Stack = createNativeStackNavigator();

const StackNavigator = () => {
  return (
    <Stack.Navigator screenOptions={{headerShown: false}}>
      <Stack.Screen name="Course" component={Home} options={{title: 'Khóa học'}} />
      <Stack.Screen name="Lesson" component={Lessons} options={{title: 'Bài học'}} />
    </Stack.Navigator>
  );
}

const Tab = createBottomTabNavigator();
const TabNavigator = () => {
  const [user, ] = useContext(MyUserContext);

  return (
    <Tab.Navigator>
      <Tab.Screen name="Home" component={StackNavigator} options={{title: "Khóa học", tabBarIcon: () => <Icon source="home" size={30} color="blue" />}} />

      {user === null?<>
        <Tab.Screen name="Register" component={Register} options={{title: "Đăng ký", tabBarIcon: () => <Icon source="account" size={30} color="blue" />}} />
        <Tab.Screen name="Login" component={Login} options={{title: "Đăng nhập", tabBarIcon: () => <Icon source="login" size={30} color="blue" />}} />
      </>:<>
        <Tab.Screen name="Profile" component={Profile} options={{title: "Người dùng", tabBarIcon: () => <Icon source="account" size={30} color="blue" />}} />
      </>}
      
    </Tab.Navigator>
  );
}

const App = () => {
  const [user, dispatch] = useReducer(MyUserReducer, null);

  return (
    <MyUserContext.Provider value={[user, dispatch]}>
      <NavigationContainer>
        <TabNavigator />
      </NavigationContainer>
    </MyUserContext.Provider>
  );
}

export default App;