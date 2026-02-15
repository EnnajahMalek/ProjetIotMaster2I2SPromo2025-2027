import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { useRouter } from "expo-router";
import { useContext } from "react";
import { AuthContext } from "../../context/AuthContext";

export default function Profile() {
  const router = useRouter();
  const { user } = useContext(AuthContext);

  return (
    <ScrollView style={styles.container}>
      
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()}>
          <Ionicons name="arrow-back" size={24} color="#000" />
        </TouchableOpacity>
        <Text style={styles.title}>Profile</Text>
      </View>

      {/* User Card */}
      <View style={styles.card}>
        <Ionicons name="person-circle" size={80} color="#C8A27C" />
        <Text style={styles.name}>Smart Home User</Text>
        <Text style={styles.email}>{user?.email}</Text>
      </View>

      {/* Smart Home Info */}
      <Text style={styles.sectionTitle}>Smart Home Information</Text>

      <View style={styles.infoCard}>
        <InfoRow label="Home Name" value="ADCP Smart Home" />
        <InfoRow label="Location" value="My House" />
        <InfoRow label="Active Modes" value="Normal, Nuit" />
        <InfoRow label="Connected Devices" value="8 Devices" />
      </View>

      {/* System Info */}
      <Text style={styles.sectionTitle}>System</Text>

      <View style={styles.infoCard}>
        <InfoRow label="Platform" value="IoT ADCP" />
        <InfoRow label="Version" value="1.0.0" />
        <InfoRow label="Status" value="Active" />
      </View>
    </ScrollView>
  );
}
function InfoRow({ label, value }) {
  return (
    <View style={styles.row}>
      <Text style={styles.label}>{label}</Text>
      <Text style={styles.value}>{value}</Text>
    </View>
  );
}
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#EFEAE6",
    padding: 20,
  },

  header: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 20,
  },

  title: {
    fontSize: 20,
    fontWeight: "600",
    marginLeft: 10,
  },

  card: {
    backgroundColor: "#fff",
    borderRadius: 24,
    padding: 20,
    alignItems: "center",
    marginBottom: 25,
  },

  name: {
    fontSize: 18,
    fontWeight: "600",
    marginTop: 10,
  },

  email: {
    color: "#777",
    marginTop: 4,
  },

  sectionTitle: {
    fontSize: 18,
    fontWeight: "600",
    marginBottom: 12,
  },

  infoCard: {
    backgroundColor: "#fff",
    borderRadius: 20,
    padding: 16,
    marginBottom: 20,
  },

  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    paddingVertical: 8,
  },

  label: {
    color: "#555",
  },

  value: {
    fontWeight: "600",
  },
});