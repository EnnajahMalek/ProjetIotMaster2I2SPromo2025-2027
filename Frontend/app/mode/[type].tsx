import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from "react-native";
import { useLocalSearchParams, useRouter } from "expo-router";
import { Ionicons } from "@expo/vector-icons";

const MODES = {
  normal: {
    title: "Mode Normal",
    description:
      "Mode principal de la maison. Il assure le confort et la sécurité.",
    sensors: ["Température", "Humidité", "Gaz", "Activité"],
    actions: [
      "Activation automatique de la climatisation",
      "Activation du chauffage",
      "Ouverture des fenêtres",
      "Envoi de notifications",
    ],
  },
  nuit: {
    title: "Mode Nuit",
    description:
      "Mode actif pendant la nuit pour assurer la sécurité des occupants.",
    sensors: ["Mouvement", "Présence chambre"],
    actions: [
      "Détection de sortie nocturne",
      "Allumage automatique des lumières",
      "Notification immédiate",
    ],
  },
  enfants: {
    title: "Mode Enfants",
    description:
      "Mode dédié à la sécurité des enfants à l’intérieur du domicile.",
    sensors: ["Capteur de porte"],
    actions: [
      "Détection ouverture de porte",
      "Notification immédiate",
      "Ouverture automatique (optionnelle)",
    ],
  },
};

export default function ModeDetails() {
  const { type } = useLocalSearchParams();
  const router = useRouter();

  const mode = MODES[type];

  if (!mode) {
    return (
      <View style={styles.container}>
        <Text>Mode not found</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()}>
          <Ionicons name="arrow-back" size={24} color="#000" />
        </TouchableOpacity>
        <Text style={styles.title}>{mode.title}</Text>
      </View>

      {/* Description */}
      <View style={styles.card}>
        <Text style={styles.sectionTitle}>Description</Text>
        <Text style={styles.text}>{mode.description}</Text>
      </View>

      {/* Sensors */}
      <View style={styles.card}>
        <Text style={styles.sectionTitle}>Capteurs actifs</Text>
        {mode.sensors.map((s, i) => (
          <Text key={i} style={styles.listItem}>• {s}</Text>
        ))}
      </View>

      {/* Actions */}
      <View style={styles.card}>
        <Text style={styles.sectionTitle}>Actions automatiques</Text>
        {mode.actions.map((a, i) => (
          <Text key={i} style={styles.listItem}>• {a}</Text>
        ))}
      </View>
    </ScrollView>
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
    borderRadius: 20,
    padding: 16,
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: "600",
    marginBottom: 8,
  },
  text: {
    color: "#555",
  },
  listItem: {
    marginVertical: 4,
    color: "#444",
  },
});
