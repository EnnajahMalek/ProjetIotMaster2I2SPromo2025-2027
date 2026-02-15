import { Ionicons } from "@expo/vector-icons";
import { BlurView } from "expo-blur";
import { useRouter } from "expo-router";
import { useContext, useState } from "react";
import {
  Alert,
  Image,
  ImageBackground,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";
import { AuthContext } from "../../context/AuthContext";
import AsyncStorage from "@react-native-async-storage/async-storage";

export default function Login() {
  const router = useRouter();
  const { login } = useContext(AuthContext);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const handleLogin = async () => {
  console.log("Login pressed");

  if (!email || !password) {
    Alert.alert("Error", "Please enter email and password");
    return;
  }

  try {
    const response = await fetch("https://backendiotproject-c4gbdtdqcebjb9c9.spaincentral-01.azurewebsites.net/api/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ "email": email,"password": password }),
    });

    console.log("Status:", response.status);

    const data = await response.json();
    console.log("Server response:", data);

    if (!response.ok) {
      Alert.alert("Login failed", data.message || "Invalid credentials");
      return;
    }

    // save token
    await AsyncStorage.setItem("authToken", data.token);
    console.log("Token saved:", data.token);

    // update context if you use it
    if (login) await login(data.token);

    router.replace("/(tabs)");


  } catch (error) {
    console.log("Network error:", error);
    Alert.alert("Connection error", "Cannot reach server");
  }
};


  return (
    <ImageBackground
      source={require("../../assets/images/blur-bg.jpg")}
      resizeMode="cover"
      style={styles.bg}
    >
      {/* Blur iOS */}
      <BlurView intensity={45} tint="light" style={StyleSheet.absoluteFill} />

      {/* Overlay beige */}
      <View style={styles.overlay} />

      {/* LOGO (plus élégant) */}
      <View style={styles.logoContainer}>
        <View style={styles.logoGlass}>
          <Image
            source={require("../../assets/images/logo-iot.png")}
            style={styles.logo}
          />
        </View>

        {/* ✅ On garde seulement le slogan (pas de Welcome, pas de chip) */}
        <Text style={styles.welcomeSubtitle}>Control • Connect • Innovate</Text>
        <Text style={styles.welcomeHint}>login to manage your smart home</Text>
      </View>

      {/* FORMULAIRE */}
      <View style={styles.formWrapper}>
        <View style={styles.card}>
          {/* Email */}
          <View style={styles.inputRow}>
            <View style={styles.leftIcon}>
              <Ionicons name="mail-outline" size={18} color="#6B4F3A" />
            </View>
            <TextInput
              placeholder="Email"
              placeholderTextColor="#8A7D72"
              value={email}
              onChangeText={setEmail}
              style={styles.input}
              keyboardType="email-address"
              autoCapitalize="none"
            />
          </View>

          {/* Password */}
          <View style={styles.inputRow}>
            <View style={styles.leftIcon}>
              <Ionicons name="lock-closed-outline" size={18} color="#6B4F3A" />
            </View>
            <TextInput
              placeholder="Password"
              placeholderTextColor="#8A7D72"
              value={password}
              onChangeText={setPassword}
              style={styles.input}
              secureTextEntry={!showPassword}
            />
            <TouchableOpacity
              onPress={() => setShowPassword(!showPassword)}
              style={styles.rightIcon}
              activeOpacity={0.7}
            >
              <Ionicons
                name={showPassword ? "eye-off-outline" : "eye-outline"}
                size={20}
                color="#6B4F3A"
              />
            </TouchableOpacity>
          </View>

          {/* Button */}
          <TouchableOpacity style={styles.button} onPress={handleLogin}>
            <Text style={styles.buttonText}>LOGIN</Text>
          </TouchableOpacity>
        </View>
      </View>
    </ImageBackground>
  );
}

const styles = StyleSheet.create({
  bg: {
    flex: 1,
  },

  overlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: "rgba(239,234,230,0.25)",
  },

  /* LOGO */
  logoContainer: {
    marginTop: 75,
    alignItems: "center",
  },

  logo: {
    width: 300,
    height: 200,
    resizeMode: "contain",
  },

  /* TEXT sous logo */
  welcomeSubtitle: {
    marginTop: 14,
    fontSize: 14,
    color: "rgba(255, 255, 255, 0.85)",
    textAlign: "center",
    letterSpacing: 4.2,
  },

  welcomeHint: {
    marginTop: 6,
    fontSize: 13,
    color: "rgba(255,255,255,0.7)",
    textAlign: "center",
  },

  /* FORM */
  formWrapper: {
    paddingHorizontal: 22,
    marginTop: 100,
  },

  card: {
    backgroundColor: "rgba(255,255,255,0.28)",
    borderRadius: 26,
    padding: 18,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.45)",
    shadowColor: "#000",
    shadowOpacity: 0.25,
    shadowRadius: 24,
    shadowOffset: { width: 0, height: 14 },
    elevation: 12,
  },

  inputRow: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "rgba(255,255,255,0.7)",
    borderRadius: 14,
    borderWidth: 1,
    borderColor: "rgba(217,207,196,0.9)",
    marginTop: 14,
  },

  leftIcon: {
    width: 46,
    height: 48,
    justifyContent: "center",
    alignItems: "center",
    borderRightWidth: 1,
    borderRightColor: "rgba(130,105,85,0.2)",
  },

  rightIcon: {
    width: 46,
    height: 48,
    justifyContent: "center",
    alignItems: "center",
    borderLeftWidth: 1,
    borderLeftColor: "rgba(130,105,85,0.2)",
  },

  input: {
    flex: 1,
    height: 48,
    paddingHorizontal: 12,
    color: "#2A2018",
    fontSize: 15,
  },

  button: {
    marginTop: 22,
    backgroundColor: "#6B4F3A",
    height: 50,
    borderRadius: 14,
    justifyContent: "center",
    alignItems: "center",
  },

  buttonText: {
    color: "#F6F1EC",
    fontWeight: "700",
    letterSpacing: 1.4,
  },
});
