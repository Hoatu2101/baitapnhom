import { useEffect, useState } from "react";
import { ActivityIndicator, FlatList, View } from "react-native";

import { List } from "react-native-paper";
import { Image } from "react-native";

import { useRoute } from "@react-navigation/native";
import Apis, { endpoints } from "../../utils/Apis";
import MyStyles from "../../styles/MyStyles";

const Lessons = () => {
    const [lessons, setLessons] = useState([]);
    const [loading, setLoading] = useState(false);
    const route = useRoute();
    const courseId = route?.params?.courseId;

    const loadLessons = async () => {
        try {
            setLoading(true); 

          
            let res = await Apis.get(endpoints['lessons'](courseId));

            setLessons(res.data);
        } catch (ex) {
            console.error(ex);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
       loadLessons()
    }, [courseId]);

    return (
        <View style={MyStyles.padding}>
            <FlatList 
                ListFooterComponent={loading && <ActivityIndicator size="large" />} 
                data={lessons}
                renderItem={({item}) => <List.Item key={item.id}
                                                title={item.subject}
                                                description={item.created_date}
                                                left={() => <Image style={MyStyles.avatar} source={{uri: item.image}} />}
                                            />}
                />
        </View>
    )
}

export default Lessons;