import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Switch,
  TouchableOpacity,
  Alert,
  RefreshControl,
  Animated,
  Easing,
} from "react-native";
import { useContext, useState, useEffect, useCallback, useRef } from "react";
import { useRouter } from "expo-router";
import { AuthContext } from "../../context/AuthContext";
import { Ionicons, MaterialIcons, FontAwesome5 } from "@expo/vector-icons";
import AsyncStorage from "@react-native-async-storage/async-storage";
import * as Notifications from "expo-notifications";

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowBanner: true,
    shouldShowList: true,
    shouldPlaySound: true,
    shouldSetBadge: false,
  }),
});

export default function Dashboard() {
  const { logout } = useContext(AuthContext);
  const router = useRouter();

  const [modeNormal, setModeNormal] = useState(true);
  const [modeNuit, setModeNuit] = useState(false);
  const [modeEnfants, setModeEnfants] = useState(false);
  const [temperature, setTemperatureState] = useState("--");
  const [shownNotifications, setShownNotifications] = useState(new Set());
  const [refreshing, setRefreshing] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const screenOpacity = useRef(new Animated.Value(0)).current;
  const screenTranslateY = useRef(new Animated.Value(18)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(screenOpacity, {
        toValue: 1,
        duration: 550,
        easing: Easing.out(Easing.cubic),
        useNativeDriver: true,
      }),
      Animated.timing(screenTranslateY, {
        toValue: 0,
        duration: 550,
        easing: Easing.out(Easing.cubic),
        useNativeDriver: true,
      }),
    ]).start();
  }, [screenOpacity, screenTranslateY]);

  useEffect(() => {
    const requestPermission = async () => {
      const { status } = await Notifications.requestPermissionsAsync();
      if (status !== "granted") {
        console.log("Notification permission not granted");
      }
    };

    requestPermission();
  }, []);

  const handleLogout = () => {
    logout();
    router.replace("/auth/login"); 
  };

  const loadTemperature = async () => {
    try {
      const token = await AsyncStorage.getItem("authToken");

      const response = await fetch(
        "https://backendiotproject-c4gbdtdqcebjb9c9.spaincentral-01.azurewebsites.net/api/temperature/livingroom",
        
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      console.log(response);
      console.log("GET status:", response.status);

      if (!response.ok) return;

      const data = await response.json();
      console.log("Temperature data:", data);

      setTemperatureState(parseFloat(data.value).toFixed(1));

    } catch (err) {
      console.log("Load temp error:", err);
    }
  };

  const checkNotifications = async () => {
    try {
      const token = await AsyncStorage.getItem("authToken");

      const response = await fetch(
        "https://backendiotproject-c4gbdtdqcebjb9c9.spaincentral-01.azurewebsites.net/api/device/unread",
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) return;

      const notifications = await response.json();

      for (const notif of notifications) {
        setShownNotifications(prev => {
          if (prev.has(notif.id)) return prev;
      
          const updated = new Set(prev);
          updated.add(notif.id);

          Notifications.scheduleNotificationAsync({
            content: {
              title: notif.alertType,
              body: notif.body,
              sound: "default",
            },
            trigger: null,
          });

          return updated;
        });
      }

    } catch (err) {
      console.log("Notification check error:", err);
    }
  };

  const onRefresh = useCallback(async () => {
    setRefreshing(true);
    try {
      // Load main temperature
      await loadTemperature();
      
      // Check for new notifications
      await checkNotifications();
      
      // Trigger refresh for all RoomCard components
      setRefreshTrigger(prev => prev + 1);
      
      console.log("All data refreshed");
    } catch (error) {
      console.log("Refresh error:", error);
    } finally {
      setRefreshing(false);
    }
  }, []);
 
  useEffect(() => {
    loadTemperature();
    checkNotifications();

    const interval = setInterval(checkNotifications, 10000);

    return () => clearInterval(interval);
  }, []);

  // ✅ Create notification in backend (for mode toggles)
  const createNotification = async (title, body) => {
    try {
      const token = await AsyncStorage.getItem("authToken");
      
      await fetch(
        "https://backendiotproject-c4gbdtdqcebjb9c9.spaincentral-01.azurewebsites.net/api/device/send",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            topic: "mode-change",
            title: title,
            alert: {
              roomId: "home",
              type: "Light", // Generic type for mode changes
              severity: "NORMAL",
              description: body,
              is_anomaly: false
            },
            timestamp: new Date().toISOString()
          })
        }
      );
      
      console.log("Notification created in backend");
    } catch (err) {
      console.log("Error creating notification:", err);
    }
  };
 
  const sendNotification = useCallback(async (title, body) => {
   
    // Alert.alert(title, body);
     
    await createNotification(title, body);
  }, []);

  return (
    <Animated.View
      style={{
        flex: 1,
        opacity: screenOpacity,
        transform: [{ translateY: screenTranslateY }],
      }}
    >
      <ScrollView 
        style={styles.container} 
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            tintColor="#C8A27C"
            colors={["#C8A27C"]}
          />
        }
      >
      
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.brandBlock}>
          <View style={styles.brandRow}>
            <Text style={styles.title}>IoT Smart Home</Text>
          </View>
        </View>
        <View style={styles.headerActions}>
          <TouchableOpacity
            style={styles.profile}
            onPress={() => router.push("/profile")}
          >
            <Ionicons name="person" size={22} color="#fff" />
          </TouchableOpacity>
          <TouchableOpacity style={styles.logoutBtn} onPress={handleLogout}>
            <Ionicons name="log-out-outline" size={22} color="#fff" />
          </TouchableOpacity>
        </View>
      </View>

      {/* Welcome */}
      <View style={styles.welcome}>
        <View>
          <Text style={styles.temp}>{temperature}°</Text>
          <Text style={styles.subtitle}>Welcome to your Smart Home</Text>
        </View>
      </View>

      {/* Rooms */}
      <Text style={styles.sectionTitle}>All Rooms</Text>
      <ScrollView horizontal showsHorizontalScrollIndicator={false}>
        <RoomCard id="livingroom" title="Living Room" refreshTrigger={refreshTrigger} />
        <RoomCard id="kitchen" title="Kitchen" refreshTrigger={refreshTrigger} />
        <RoomCard id="bedroom" title="Bedroom" refreshTrigger={refreshTrigger} />
        <RoomCard id="toilet" title="Bathroom" refreshTrigger={refreshTrigger} />
      </ScrollView>

      {/* Modes */}
      <Text style={styles.sectionTitle}>Modes</Text>

      <ModeCard
        type="normal"
        icon="home-outline"
        title="Mode Normal"
        description="Température, humidité, gaz"
        value={modeNormal}
        onChange={(value) => {
          setModeNormal(value);
          if (value) {
            sendNotification(
              "🏠 Mode Normal activé",
              "Le mode normal de la maison est activé"
            );
          }
        }}
      />

      <ModeCard
        type="nuit"
        icon="moon-outline"
        title="Mode Nuit"
        description="Surveillance nocturne"
        value={modeNuit}
        onChange={(value) => {
          setModeNuit(value);
          if (value) {
            sendNotification(
              "🌙 Mode Nuit activé",
              "La surveillance nocturne est activée"
            );
          }
          router.push({
            pathname: "/room/living",
            params: { modeNuit: value ? "on" : "off" },
          });
        }}
      />

      <ModeCard
        type="enfants"
        icon="happy-outline"
        title="Mode Enfants"
        description="Sécurité des enfants"
        value={modeEnfants}
        onChange={(value) => {
          setModeEnfants(value);
          if (value) {
            sendNotification(
              "🧒 Mode Enfants activé",
              "La sécurité enfants est maintenant active"
            );
          }
        }}
      />
      </ScrollView>
    </Animated.View>
  );
}

function RoomCard({ id, title, refreshTrigger }) {
  const router = useRouter();
  const [temp, setTemp] = useState("--");
  const [humidity, setHumidity] = useState("--");

  const loadRoomData = useCallback(async () => {
    try {
      const token = await AsyncStorage.getItem("authToken");

      const tempRes = await fetch(
        `https://backendiotproject-c4gbdtdqcebjb9c9.spaincentral-01.azurewebsites.net/api/temperature/${id}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (tempRes.ok) {
        const tempData = await tempRes.json();
        if (tempData?.value) {
          setTemp(parseFloat(tempData.value).toFixed(1));
        }
      }

      const humRes = await fetch(
        `https://backendiotproject-c4gbdtdqcebjb9c9.spaincentral-01.azurewebsites.net/api/humidity/${id}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (humRes.ok) {
        const humData = await humRes.json();
        if (humData?.value) {
          setHumidity(parseFloat(humData.value).toFixed(0));
        }
      }

    } catch (err) {
      console.log("Room data error:", err);
    }
  }, [id]);

  useEffect(() => {
    loadRoomData();
  }, [id, refreshTrigger, loadRoomData]);

  return (
    <TouchableOpacity
      style={styles.roomCard}
      onPress={() => router.push(`/room/${id}`)}
      activeOpacity={0.9}
    >
      <Text style={styles.roomTitle}>{title}</Text>
      <View style={styles.centerData}>
        <Text style={styles.roomTemp}>{temp}°</Text>
        <Text style={styles.roomHumidity}>💧 {humidity}%</Text>
      </View>
      <View style={styles.roomFooter}>
        <Ionicons name="thermometer-outline" size={18} color="#fff" />
        <Ionicons name="wifi-outline" size={18} color="#fff" />
      </View>
    </TouchableOpacity>
  );
}

function Device({ icon, label }) {
  return (
    <TouchableOpacity style={styles.device}>
      {icon === "fan" ? (
        <FontAwesome5 name="fan" size={24} color="#fff" />
      ) : (
        <MaterialIcons name={icon} size={26} color="#fff" />
      )}
      <Text style={styles.deviceText}>{label}</Text>
    </TouchableOpacity>
  );
}

function ModeCard({ type, icon, title, description, value, onChange }) {
  const router = useRouter();

  return (
    <TouchableOpacity
      style={styles.modeCard}
      onPress={() => router.push(`/mode/${type}`)}
      activeOpacity={0.8}
    >
      <View style={styles.modeLeft}>
        <View style={styles.iconBox}>
          <Ionicons name={icon} size={22} color="#fff" />
        </View>
        <View>
          <Text style={styles.modeTitle}>{title}</Text>
          <Text style={styles.modeDesc}>{description}</Text>
        </View>
      </View>
      <Switch value={value} onValueChange={onChange} />
    </TouchableOpacity>
  );
}

 
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#EFEAE6",
    padding: 20,
  },

  title: {
    fontSize: 24,
    fontWeight: "700",
    color: "#8A6A4A",
    marginLeft: 10,
  },

  brandBlock: {
    flexShrink: 1,
    marginTop: 25,
   
  },

  brandRow: {
    flexDirection: "row",
    alignItems: "center",
  },

  text: {
    fontSize: 16,
  },

  logoutBtn: {
    backgroundColor: "#C8A27C",
    padding: 10,
    borderRadius: 12,
  },

  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-start",
    marginBottom: 12,
  },

  headerActions: {
    marginTop: 16,
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
  },

  welcome: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 28,
  },

  temp: {
    fontSize: 36,
    fontWeight: "bold",
  },

  subtitle: {
    color: "#666",
  },

  profile: {
    backgroundColor: "#C8A27C",
    padding: 10,
    borderRadius: 50,
  },

  sectionTitle: {
    fontSize: 18,
    fontWeight: "600",
    marginVertical: 15,
  },

  roomCard: {
    width: 220,
    height: 260,
    backgroundColor: "#BFA38A",
    borderRadius: 30,
    padding: 20,
    marginRight: 15,
    justifyContent: "space-between",
  },

  roomTitle: {
    fontSize: 20,
    color: "#fff",
    fontWeight: "600",
  },

  roomTemp: {
    fontSize: 28,
    color: "#fff",
  },

  roomFooter: {
    flexDirection: "row",
    justifyContent: "space-between",
    width: 90,
  },

  devicesRow: {
    flexDirection: "row",
    justifyContent: "space-between",
  },

  device: {
    width: 70,
    height: 70,
    backgroundColor: "#C8A27C",
    borderRadius: 20,
    justifyContent: "center",
    alignItems: "center",
  },

  deviceText: {
    color: "#fff",
    fontSize: 12,
    marginTop: 4,
  },

  modeCard: {
    backgroundColor: "#fff",
    borderRadius: 20,
    padding: 16,
    marginBottom: 14,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },

  modeLeft: {
    flexDirection: "row",
    alignItems: "center",
  },

  iconBox: {
    backgroundColor: "#C8A27C",
    width: 42,
    height: 42,
    borderRadius: 14,
    justifyContent: "center",
    alignItems: "center",
    marginRight: 12,
  },

  modeTitle: {
    fontSize: 16,
    fontWeight: "600",
  },

  modeDesc: {
    fontSize: 13,
    color: "#777",
  },
  centerData: {
    alignItems: "left",
    justifyContent: "center",
    flex: 1,
  },

  roomTemp: {
    fontSize: 38,
    color: "#fff",
    fontWeight: "700",
  },

  roomHumidity: {
    fontSize: 16,
    color: "#fff",
    marginTop: 6,
  }
});
