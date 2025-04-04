import React from "react";
import { redirect } from "next/navigation";

const Home = () => {
  return redirect("admin/dashboard");
};

export default Home;
