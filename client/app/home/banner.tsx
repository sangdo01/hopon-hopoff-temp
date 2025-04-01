export default function Banner() {
  return (
    <div className="h-[540px] bg-[url('https://hopon-hopoff.vn/wp-content/uploads/2024/06/IMG_1303.jpg')] bg-center flex items-end justify-center">
      <div className="flex flex-col items-center mb-[58px] gap-[30px]">
        <p className="text-[50px] text-white font-bold">Hop on Hop off</p>
        <div className="w-[40vw] flex h-[56px] overflow-hidden rounded-md">
          <input className="bg-white w-[80%] px-[20px]" type="text" placeholder="Tìm kiếm" />
          <button className="w-[20%] bg-[#F20000] text-white font-bold hover:bg-[#fc4e4e] hover:cursor-pointer">Tìm kiếm</button>
        </div>
      </div>
    </div>
  );
}