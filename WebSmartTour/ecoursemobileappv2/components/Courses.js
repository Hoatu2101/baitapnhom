import { useEffect, useState } from "react";
import { ActivityIndicator, FlatList, TouchableOpacity, View } from "react-native";
import Apis, { endpoints } from "../utils/Apis";
import { List, Searchbar } from "react-native-paper";
import { Image } from "react-native";
import MyStyles from "../styles/MyStyles";
import { useNavigation } from "@react-navigation/native";

const Courses = ({cateId}) => {
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(false);
    const [q, setQ] = useState();
    const [page, setPage] = useState(1);
    const nav = useNavigation();

    const loadCourses = async () => {
        try {
            setLoading(true); 

            let url = `${endpoints['courses']}?page=${page}`;

            if (q) {
                url = `${url}&q=${q}`;
            }

            if (cateId) {
                url = `${url}&category_id=${cateId}`;
            }

            console.info(url);

            let res = await Apis.get(url);

            if (page === 1)
                setCourses(res.data.results);
            else if (page > 1)
                setCourses([...courses, ...res.data.results]);

            if (res.data.next == null)
                setPage(0);
        } catch (ex) {
            console.error(ex);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        
        let timer = setTimeout(() => {
            if (page > 0) 
                loadCourses();
        }, 500);
        

        return () => clearTimeout(timer);
    }, [q, cateId, page]);

    useEffect(() => {
        setCourses([]);
        setPage(1);
    }, [q, cateId])

    const loadMore = () => {
        if (page > 0 && !loading)
            setPage(page + 1);
    }

    return (
        <View style={MyStyles.padding}>
            <Searchbar placeholder="Tìm khóa học..." value={q} onChangeText={setQ} />
            <FlatList onEndReached={loadMore} onEndReachedThreshold={0.7}
                ListFooterComponent={loading && <ActivityIndicator size="large" />} 
                data={courses}
                renderItem={({item}) => <List.Item key={item.id}
                                                title={item.subject}
                                                description={item.created_date}
                                                left={() => <TouchableOpacity onPress={() => nav.navigate('Lesson', {courseId: item.id})}>
                                                    <Image style={MyStyles.avatar} source={{uri: item.image}} />
                                                </TouchableOpacity>}
                                            />}
                />
        </View>
    )
}

export default Courses;