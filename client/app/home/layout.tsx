import "@/styles/global.css";
import {
  AccessTime,
  Facebook,
  LocalPhone,
  Search,
  ShoppingCart,
  Store,
  Twitter,
  YouTube,
} from "@mui/icons-material";
import { title } from "process";
interface LayoutProps {
  children: React.ReactNode;
}

const menu = [
  {
    title: "Tham quan thành phố",
    link: "/",
    children: [
      { title: "TP.Hồ Chí Minh", link: "/" },
      { title: "Hà Nội", link: "/" },
    ],
  },
  {
    title: "Du lịch Việt Nam",
    link: "/about",
    children: [
      { title: "Tour tiết kiệm", link: "/" },
      { title: "Mê kông", link: "/" },
      { title: "Địa đạo Củ Chi", link: "/" },
      { title: "Cho thuê xe", link: "/" },
    ],
  },
  {
    title: "Tour nước ngoài",
    link: "/services",
    children: [
      { title: "Châu Á", link: "/" },
      { title: "Châu Âu", link: "/" },
      { title: "Châu Úc", link: "/" },
      { title: "Châu Mỹ", link: "/" },
      { title: "Europe Train", link: "/" },
    ],
  },
  {
    title: "Ticket",
    link: "/tours",
    children: [{ title: "Museum", link: "/" }],
  },
  {
    title: "Tin tức",
    link: "/contact",
    children: [{ title: "Vietnamese Food", link: "/" }],
  },
  {
    title: "Trợ giúp",
    link: "/help",
    children: [
      { title: "Khám phá", link: "/" },
      { title: "Bản đồ", link: "/" },
      { title: "Hướng dẫn mua vé online", link: "/" },
      { title: "Dành cho đại lý", link: "/" },
      { title: "Dành cho đại lý", link: "/" },
      { title: "Câu hỏi nhanh", link: "/" },
    ],
  },
  {
    title: "Về chúng tôi",
    link: "/about",
    children: [
      { title: "Ảnh Việt Nam Hop on Hop off Việt Nam", link: "/" },
      { title: "Hop on Hop off Việt Nam", link: "/" },
      { title: "Liên hệ", link: "/" },
    ],
  },
];

export default function Layout({ children }: LayoutProps) {
  return (
    <div>
      <div className="bg-[url('https://hopon-hopoff.vn/wp-content/uploads/2017/01/new-header-e1503460071199.png')] bg-[#F20000] bg-no-repeat bg-cover bg-center fixed w-[100vw] z-[999]">
        <div className="px-[15vw] flex text-[14px] justify-between leading-[35px] text-white">
          <div className="py-[5px] gap-[20px] flex items-center">
            <p className="flex items-center gap-[5px]">
              <LocalPhone sx={{ width: "20px", height: "20px" }} />
              BOOKING ONLINE 24/7 or Call: HO CHI MINH (+84) 913 674 412/ HA NOI
              (+84) 0834 82 8833
            </p>

            <p className="flex items-center gap-[5px]">
              <AccessTime sx={{ width: "20px", height: "20px" }} />
              1:37 pm, 31st March
            </p>
          </div>
          <div className="text-white flex gap-[20px] items-center">
            <div className="flex gap-[15px] items-center text-[10px]">
              <Facebook
                sx={{
                  width: "20px",
                  height: "20px",
                  ":hover": {
                    cursor: "pointer",
                    backgroundColor: "white",
                    color: "red",
                    borderRadius: "50%",
                  },
                }}
              />
              <Twitter
                sx={{
                  width: "20px",
                  height: "20px",
                  ":hover": {
                    cursor: "pointer",
                    backgroundColor: "white",
                    color: "red",
                    borderRadius: "50%",
                  },
                }}
              />
              <YouTube
                sx={{
                  width: "20px",
                  height: "20px",
                  ":hover": {
                    cursor: "pointer",
                    backgroundColor: "white",
                    color: "red",
                    borderRadius: "50%",
                  },
                }}
              />
              <Store
                sx={{
                  width: "20px",
                  height: "20px",
                  ":hover": {
                    cursor: "pointer",
                    backgroundColor: "white",
                    color: "red",
                    borderRadius: "50%",
                  },
                }}
              />
            </div>
            <div>
              <ShoppingCart
                sx={{
                  width: "20px",
                  height: "20px",
                  ":hover": {
                    cursor: "pointer",
                    backgroundColor: "white",
                    color: "red",
                    borderRadius: "50%",
                  },
                }}
              />
            </div>
            <div>
              <Search
                sx={{
                  width: "20px",
                  height: "20px",
                  ":hover": {
                    cursor: "pointer",
                    backgroundColor: "white",
                    color: "red",
                    borderRadius: "50%",
                  },
                }}
              />
            </div>
          </div>
        </div>
        <div className="bg-[url('https://hopon-hopoff.vn/wp-content/uploads/2017/01/Saigon-50-e1503460150600.png')] bg-white bg-contain h-[86px]">
          <div className="px-[15vw]">
            <img
              src={
                "https://hopon-hopoff.vn/wp-content/uploads/2016/12/official-60x60-e1503461563520.png"
              }
              alt="logo"
              width={93}
              height={70}
            />
          </div>
        </div>
        <div className="h-[40px] px-[15vw] flex items-center uppercase font-bold text-white gap-[20px]">
          {menu.map((item, index) => {
            return (
              <div key={index} className="hover:cursor-pointer flex items-center h-[40px] group relative">
                <p>{item.title}</p>
                <div className="absolute top-[40px] scale-y-0 w-auto origin-top overflow-hidden group-hover:scale-y-100 transition-transform duration-300">
                  {item.children.map((child, index) => {
                    return (
                      <p
                        key={index}
                        className="bg-[#F20000] hover:bg-white hover:text-[#F20000] min-w-[200px] px-[20px] text-nowrap h-[40px] flex items-center"
                        style={
                          {
                            "--item-count": item.children.length,
                          } as React.CSSProperties
                        }
                      >
                        {child.title}
                      </p>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      </div>
      <div className="pt-[171px]">{children}</div>
    </div>
  );
}
