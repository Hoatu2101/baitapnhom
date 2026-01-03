import { useState } from "react";
import Categories from "../../components/Categories";
import Courses from "../../components/Courses";

const Home = () => {
    const [cateId, setCateId] = useState();

    return (
        <>
            <Categories setCateId={setCateId} />
            <Courses cateId={cateId} />
        </>
    );
}

export default Home;