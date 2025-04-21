"use client";
import {
  Button,
  FormControl,
  InputLabel,
  OutlinedInput,
  Stack,
  Typography,
} from "@mui/material";
import { useSearchParams } from "next/navigation";
import React, { useState } from "react";

const Page = () => {
  const [password, setPassword] = useState("");

  const searchParams = useSearchParams();
  const token = searchParams.get("token") || "";
  console.log("token", token);

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log(password);
    // Handle form submission logic here
    fetch("http://localhost:8000/api/reset-password-confirm", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ password, token }),
    }).then((response) => {
      if (response.ok) {
        // Password reset successful
        console.log("Password reset successful");
      } else {
        // Handle error response
        console.error("Error resetting password");
      }
    });
  };
  return (
    <Stack spacing={4}>
      <Typography>Reset password confirm page</Typography>
      <FormControl error={password.length === 0} variant="outlined" fullWidth>
        <InputLabel>Nhập mật khẩu mới</InputLabel>
        <OutlinedInput
          label="Nhập mật khẩu mới"
          type="password"
          onChange={(e) => setPassword(e.target.value)}
        />
      </FormControl>
      <Button
        variant="contained"
        color="primary"
        onClick={onSubmit}
        disabled={password.length === 0}
      >
        Xác nhận
      </Button>
    </Stack>
  );
};

export default Page;
