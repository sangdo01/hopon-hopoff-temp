import { ArrowForward } from '@mui/icons-material'
import React from 'react'


interface ITourCardProps {
  image_url: string,
  title: string,
  description: string,
  price: number,
}

function TourCard({ image_url, title, description, price }: ITourCardProps) {
  return (
    <div className='w-full h-[420px] flex flex-col bg-white rounded-md overflow-hidden group hover:cursor-pointer hover:shadow-lg hover:shadow-[#F20000] duration-300'>
      <div className=' h-[170px] w-full overflow-hidden'>
        <div style={{backgroundImage: `url(${image_url})`}} className={` bg-cover bg-bottom h-full w-full flex group-hover:scale-[130%] duration-300`}>
        </div>
      </div>
      <div className='p-[15px] flex flex-col gap-[10px] flex-1'>
        <p className='font-bold text-[20px]'>{title}</p>
        <p>{description}</p>
      </div>
      <div className='px-[15px] bg-[#F20000] text-white flex justify-end items-center gap-[20px]'>
        <p className='text-[20px] font-bold group-hover:translate-x-0 translate-x-[40px] duration-300'>{price.toLocaleString('vi-VN')}đ</p>
        <div className='group-hover:opacity-100 opacity-0 duration-300'><ArrowForward /></div>
      </div>
    </div>
  )
}

export default TourCard