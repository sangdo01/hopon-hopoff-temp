import Banner from "./banner";
import TopTour from "./toptour";

export default function Homepage() {
  return <div className="flex flex-col gap-[40px]">
    <Banner />
    <TopTour />
  </div>;
}

