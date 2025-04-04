import React, { ReactNode } from "react";
import Home from "./page";
import Header from "@/components/layouts/client/header";
import Footer from "@/components/layouts/client/footer";

const ClientLayout = ({ children }: { children: ReactNode }) => {
  return (
    <div>
      <Header />
      {children}
      <Footer />
    </div>
  );
};

export default ClientLayout;
