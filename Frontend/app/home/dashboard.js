import { View, Text, Switch } from "react-native";
import { useState } from "react";

export default function Dashboard() {
  const [modeNormal, setModeNormal] = useState(true);
  const [modeNuit, setModeNuit] = useState(false);
  const [modeEnfants, setModeEnfants] = useState(false);

  return (
    <View style={{ flex: 1, padding: 20 }}>
      
      {/* Header */}
      <View
        style={{
          flexDirection: "row",
          justifyContent: "space-between",
          marginBottom: 20,
        }}
      >
        <Text style={{ fontSize: 22 }}>🏠 ADCP</Text>
        <Text>🕒 Historique</Text>
      </View>

      {/* Modes */}
      <Text style={{ fontSize: 18, marginBottom: 10 }}>Modes</Text>

      <View style={{ flexDirection: "row", justifyContent: "space-between" }}>
        <Text>Mode Normal</Text>
        <Switch value={modeNormal} onValueChange={setModeNormal} />
      </View>

      <View style={{ flexDirection: "row", justifyContent: "space-between" }}>
        <Text>Mode Nuit</Text>
        <Switch value={modeNuit} onValueChange={setModeNuit} />
      </View>

      <View style={{ flexDirection: "row", justifyContent: "space-between" }}>
        <Text>Mode Enfants</Text>
        <Switch value={modeEnfants} onValueChange={setModeEnfants} />
      </View>
    </View>
  );
}
