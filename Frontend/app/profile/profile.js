import { router } from "expo-router";
import { useContext } from "react";
import { StyleSheet, Text, TouchableOpacity, View } from "react-native";
import { AuthContext } from "../../context/AuthContext";


export default function Profile() {
  const { user, logout } = useContext(AuthContext);

  return (
    <View style={styles.screen}>
      <Text style={styles.title}>Informations personnelles</Text>

      <View style={styles.card}>
        <Text style={styles.label}>Email</Text>
        <Text style={styles.value}>{user?.email ?? "Non connecté"}</Text>
      </View>

      <TouchableOpacity
        style={styles.btn}
        onPress={() => {
          logout?.();
          router.replace("/auth/login");
        }}
      >
        <Text style={styles.btnText}>Se déconnecter</Text>
      </TouchableOpacity>
    </View>
  );
}

const COLORS = {
  bg: "#EFE7DE",
  card: "#FFFFFF",
  text: "#2B2725",
  muted: "#6E625A",
  accent: "#B89573",
};

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: COLORS.bg,
    padding: 20,
    paddingTop: 60,
  },
  title: {
    fontSize: 22,
    fontWeight: "700",
    color: COLORS.text,
    marginBottom: 16,
  },
  card: {
    backgroundColor: COLORS.card,
    borderRadius: 18,
    padding: 16,
    marginBottom: 18,
  },
  label: {
    fontSize: 12,
    color: COLORS.muted,
    marginBottom: 6,
  },
  value: {
    fontSize: 16,
    color: COLORS.text,
    fontWeight: "600",
  },
  btn: {
    backgroundColor: COLORS.accent,
    paddingVertical: 14,
    borderRadius: 16,
    alignItems: "center",
  },
  btnText: {
    color: "#fff",
    fontWeight: "700",
  },
});
