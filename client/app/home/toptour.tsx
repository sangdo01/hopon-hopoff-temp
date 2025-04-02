"use client";

import TourCard from "@/components/home/tourcard";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import "swiper/css/scrollbar";
import { Navigation, Pagination, Scrollbar, A11y } from "swiper/modules";

import { Swiper, SwiperSlide } from "swiper/react";

const tourcardData = [
  {
    image_url:
      "https://hopon-hopoff.vn/wp-content/uploads/2024/06/3T8A8769-360x240.png",
    title: "Sài Gòn - Chợ Lớn, City Tour Hop On Hop Off Tour 4H",
    description:
      "GIỚI THIỆU: Sài Gòn – Chợ Lớn City tour Hop on Hop off là tour du lịch linh hoạt và thuận tiện kết hợp ngắm cảnh TPHCM trên xe",
    price: 400000,
  },
  {
    image_url:
      "https://hopon-hopoff.vn/wp-content/uploads/2024/06/3T8A8769-360x240.png",
    title: "Sài Gòn - Phú Mỹ Hưng, City Tour 2H",
    description:
      "Khám phá khu đô thị Phú Mỹ Hưng hiện đại và sôi động với tour du lịch ngắm cảnh tuyệt đẹp.",
    price: 300000,
  },
  {
    image_url:
      "https://hopon-hopoff.vn/wp-content/uploads/2024/06/3T8A8769-360x240.png",
    title: "Sài Gòn - Bến Thành, City Tour 3H",
    description:
      "Tour du lịch Bến Thành mang đến cho bạn trải nghiệm văn hóa và ẩm thực đặc sắc của Sài Gòn.",
    price: 500000,
  },
  {
    image_url:
      "https://hopon-hopoff.vn/wp-content/uploads/2024/06/3T8A8769-360x240.png",
    title: "Sài Gòn - Nhà Thờ Đức Bà, City Tour 1H",
    description:
      "Tham quan Nhà Thờ Đức Bà, một trong những biểu tượng nổi bật của Sài Gòn với kiến trúc độc đáo.",
    price: 200000,
  },

  {
    image_url:
      "https://hopon-hopoff.vn/wp-content/uploads/2024/06/3T8A8769-360x240.png",
    title: "Khám Phá Bến Thành - Tour 2 Giờ",
    description:
      "Tham gia tour khám phá chợ Bến Thành, nơi bạn có thể tìm thấy những món quà lưu niệm độc đáo và thưởng thức ẩm thực đường phố đặc sắc.",
    price: 250000,
  },

  {
    image_url:
      "https://hopon-hopoff.vn/wp-content/uploads/2024/06/3T8A8769-360x240.png",
    title: "Tour Tham Quan Phú Mỹ Hưng - 3 Giờ",
    description:
      "Khám phá khu đô thị Phú Mỹ Hưng hiện đại với những công trình kiến trúc độc đáo và không gian xanh mát.",
    price: 300000,
  },

  {
    image_url:
      "https://hopon-hopoff.vn/wp-content/uploads/2024/06/3T8A8769-360x240.png",
    title: "Tour Văn Hóa Ẩm Thực Sài Gòn - 4 Giờ",
    description:
      "Tham gia tour ẩm thực để trải nghiệm những món ăn đặc sản của Sài Gòn, từ phở đến bánh mì.",
    price: 400000,
  },

  {
    image_url:
      "https://hopon-hopoff.vn/wp-content/uploads/2024/06/3T8A8769-360x240.png",
    title: "Khám Phá Nhà Thờ Đức Bà - Tour 1 Giờ",
    description:
      "Khám phá vẻ đẹp kiến trúc của Nhà Thờ Đức Bà, một trong những biểu tượng văn hóa đặc sắc của Sài Gòn.",
    price: 200000,
  },

  {
    image_url:
      "https://hopon-hopoff.vn/wp-content/uploads/2024/06/3T8A8769-360x240.png",
    title: "Tour Tham Quan Khu Phố Tây - 2 Giờ",
    description:
      "Khám phá khu phố Tây Bùi Viện, nơi nổi tiếng với cuộc sống về đêm sôi động và đa dạng văn hóa.",
    price: 180000,
  },
  {
    image_url:
      "https://hopon-hopoff.vn/wp-content/uploads/2024/06/3T8A8769-360x240.png",
    title: "Tour Tham Quan Củ Chi - 5 Giờ",
    description:
      "Khám phá hệ thống địa đạo Củ Chi, nơi từng là căn cứ của quân đội Việt Nam trong thời kỳ chiến tranh.",
    price: 350000,
  },
];

export default function TopTour() {
  return (
    <div className="px-[15vw] pb-[50px] bg-[#F6F6F6] flex flex-col gap-[20px]">
      <div className="flex justify-center">
        <p className="text-[40px] font-bold text-gray-600 border-b-4 border-[#F20000]">
          Tour được đặt nhiều nhất
        </p>
      </div>
      <Swiper
        modules={[Navigation]}
        spaceBetween={50}
        slidesPerView={3}
        navigation
        onSwiper={(swiper) => console.log(swiper)}
        onSlideChange={() => console.log("slide change")}
        className="w-full"
      >
        {tourcardData.map((tour, index) => (
          <SwiperSlide key={index}>
            <TourCard
              image_url={tour.image_url}
              title={tour.title}
              description={tour.description}
              price={tour.price}
            />
          </SwiperSlide>
        ))}
      </Swiper>
  
    </div>
  );
}
