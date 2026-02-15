import { Redirect } from "expo-router";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";


export default function Index() {
  const { user } = useContext(AuthContext);

  if (!user) {
    return <Redirect href="/auth/login" />;
  }

  return <Redirect href="/home/dashboard" />;
}
