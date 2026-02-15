import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Dimensions,
  TouchableOpacity,
  Switch,
  ActivityIndicator,
  RefreshControl,
} from "react-native";
import { useLocalSearchParams, useFocusEffect } from "expo-router";
import { LineChart } from "react-native-chart-kit";
import * as Notifications from "expo-notifications";
import { useEffect, useState, useCallback, useRef } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";

const screenWidth = Dimensions.get("window").width;

const API_BASE_TEMP = "https://backendiotproject-c4gbdtdqcebjb9c9.spaincentral-01.azurewebsites.net/api/temperature";
const API_BASE_ROOM = "https://backendiotproject-c4gbdtdqcebjb9c9.spaincentral-01.azurewebsites.net/api/room";

export default function RoomHistory() {
  const params = useLocalSearchParams();
  const id = Array.isArray(params.id) ? params.id[0] : params.id;
  const modeNuit = Array.isArray(params.modeNuit) ? params.modeNuit[0] : params.modeNuit;
  const isNightMode = modeNuit === "on";

  const TEMP_THRESHOLD = 28;
  const GAS_THRESHOLD = 15;

  const [climOn, setClimOn] = useState<boolean | null>(null);
  const [temperatureData, setTemperatureData] = useState([]);
  const [humidityData, setHumidityData] = useState([]);
  const [labels, setLabels] = useState([]);
  const [lightOn, setLightOn] = useState<boolean | null>(null);
  const [windowOpen, setWindowOpen] = useState<boolean | null>(null);
  const [targetTemp, setTargetTemp] = useState<number | null>(null);
  const [currentTemp, setCurrentTemp] = useState<number | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  // Use refs to track if we've applied night mode automation
  const hasAppliedNightMode = useRef(false);
  const hasAppliedTempAlert = useRef(false);

  const isTempAlert =
    temperatureData.length > 0 &&
    Math.max(...temperatureData) > TEMP_THRESHOLD;

  // Get auth headers
  const getAuthHeaders = async () => {
    const token = await AsyncStorage.getItem("authToken");
    return {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    };
  };

  // Fetch current temperature
  const fetchCurrentTemperature = useCallback(async () => {
    if (!id) return;

    try {
      const headers = await getAuthHeaders();
      const response = await fetch(
        `https://backendiotproject-c4gbdtdqcebjb9c9.spaincentral-01.azurewebsites.net/api/temperature/${id}`,
        { headers }
      );

      if (response.ok) {
        const data = await response.json();
        // API returns: {"key": "Temperature", "value": "31.65"}
        const temp = parseFloat(data.value);
        setCurrentTemp(temp);
      } else {
        console.error("Failed to fetch current temperature");
      }
    } catch (error) {
      console.error("Error fetching current temperature:", error);
    }
  }, [id]);

  // Fetch all initial states
  const fetchAllStates = useCallback(async () => {
    if (!id) return;

    try {
      const headers = await getAuthHeaders();

      // Fetch temperature preference
      const tempResponse = await fetch(`${API_BASE_TEMP}/get-preference/${id}`);
      if (tempResponse.ok) {
        const tempData = await tempResponse.json();
        setTargetTemp(typeof tempData === 'number' ? tempData : tempData.temperature ?? 22);
      } else {
        setTargetTemp(22);
      }

      // Fetch light status
      const lightResponse = await fetch(`${API_BASE_ROOM}/light/${id}`, { headers });
      if (lightResponse.ok) {
        const lightData = await lightResponse.json();
        setLightOn(lightData);
      } else {
        setLightOn(false);
      }

      // Fetch AC/climat status
      const climatResponse = await fetch(`${API_BASE_ROOM}/climat/${id}`, { headers });
      if (climatResponse.ok) {
        const climatData = await climatResponse.json();
        setClimOn(climatData);
      } else {
        setClimOn(false);
      }

      // Fetch window status
      const windowResponse = await fetch(`${API_BASE_ROOM}/window/${id}`, { headers });
      if (windowResponse.ok) {
        const windowData = await windowResponse.json();
        setWindowOpen(windowData);
      } else {
        setWindowOpen(false);
      }
    } catch (error) {
      console.error("Error fetching initial states:", error);
      // Set fallback values
      setTargetTemp(22);
      setLightOn(false);
      setClimOn(false);
      setWindowOpen(false);
    }
  }, [id]);

  // Load temperature graph
  const loadTemperatureGraph = useCallback(async () => {
    if (!id) return;

    try {
      const token = await AsyncStorage.getItem("authToken");

      const response = await fetch(
        `https://backendiotproject-c4gbdtdqcebjb9c9.spaincentral-01.azurewebsites.net/api/temperature/${id}/graph?minutes=1440`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        console.log("Temperature request failed");
        return;
      }

      const data = await response.json();

      if (!data?.points?.length) {
        setTemperatureData([]);
        return;
      }

      const values = data.points.map(p => Number(p.value));
      const timeLabels = data.points.map(p =>
        p.timestamp.slice(11, 16)
      );

      setTemperatureData(values);
      setLabels(timeLabels);

    } catch (err) {
      console.log("Temperature graph error:", err);
    }
  }, [id]);

  // Load humidity graph
  const loadHumidityGraph = useCallback(async () => {
    if (!id) return;

    try {
      const token = await AsyncStorage.getItem("authToken");

      const response = await fetch(
        `https://backendiotproject-c4gbdtdqcebjb9c9.spaincentral-01.azurewebsites.net/api/humidity/${id}/graph?minutes=1440`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        console.log("Humidity request failed");
        return;
      }

      const data = await response.json();

      if (!data?.points?.length) {
        setHumidityData([]);
        return;
      }

      const values = data.points.map(p => Number(p.value));
      setHumidityData(values);

    } catch (err) {
      console.log("Humidity graph error:", err);
    }
  }, [id]);

  // Unified refresh function
  const onRefresh = useCallback(async () => {
    setRefreshing(true);
    await Promise.all([
      fetchCurrentTemperature(),
      fetchAllStates(),
      loadTemperatureGraph(),
      loadHumidityGraph(),
    ]);
    setRefreshing(false);
  }, [fetchCurrentTemperature, fetchAllStates, loadTemperatureGraph, loadHumidityGraph]);

  // Fetch states on mount
  useEffect(() => {
    fetchCurrentTemperature();
    fetchAllStates();
    loadTemperatureGraph();
    loadHumidityGraph();
  }, [fetchCurrentTemperature, fetchAllStates, loadTemperatureGraph, loadHumidityGraph]);

  // Refetch states when screen comes into focus
  useFocusEffect(
    useCallback(() => {
      fetchCurrentTemperature();
      fetchAllStates();
      loadTemperatureGraph();
      loadHumidityGraph();
      // Reset automation flags when screen refocuses
      hasAppliedNightMode.current = false;
      hasAppliedTempAlert.current = false;
    }, [fetchCurrentTemperature, fetchAllStates, loadTemperatureGraph, loadHumidityGraph])
  );

  const updateTemperaturePreference = async (newTemp: number) => {
    if (!id) return;
    
    try {
      const response = await fetch(`${API_BASE_TEMP}/set-preference/${id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ temperature: newTemp }),
      });

      if (!response.ok) {
        console.error("Failed to update temperature preference");
      }
    } catch (error) {
      console.error("Error updating temperature:", error);
    }
  };

  const handleTempChange = (delta: number) => {
    if (targetTemp === null) return;
    
    const newTemp = targetTemp + delta;
    setTargetTemp(newTemp);
    updateTemperaturePreference(newTemp);
  };

  const toggleLight = async () => {
    if (!id || lightOn === null) return;
    
    const newState = !lightOn;
    
    // Update UI immediately for instant feedback
    setLightOn(newState);
    
    // Make API call in background - don't await or block
    const headers = await getAuthHeaders();
    const url = `${API_BASE_ROOM}/light/toggle/${id}`;
    
    fetch(url, {
      method: "POST",
      headers,
    }).catch(error => {
      // Silently revert on error
      setLightOn(!newState);
      console.error("Error toggling light:", error);
    });
  };

  const toggleClimat = async (newValue: boolean) => {
    if (!id || climOn === null) return;
    
    // Update UI immediately for instant feedback
    setClimOn(newValue);
    
    // Make API call in background - don't await or block
    const headers = await getAuthHeaders();
    const url = `${API_BASE_ROOM}/climat/toggle/${id}`;
    
    fetch(url, {
      method: "POST",
      headers,
    }).catch(error => {
      // Silently revert on error
      setClimOn(!newValue);
      console.error("Error toggling climate:", error);
    });
  };

  const toggleWindow = async () => {
    if (!id || windowOpen === null) return;
    
    const newState = !windowOpen;
    
    // Update UI immediately for instant feedback
    setWindowOpen(newState);
    
    // Make API call in background - don't await or block
    const headers = await getAuthHeaders();
    const url = `${API_BASE_ROOM}/window/toggle/${id}`;
    
    fetch(url, {
      method: "POST",
      headers,
    }).catch(error => {
      // Silently revert on error
      setWindowOpen(!newState);
      console.error("Error toggling window:", error);
    });
  };

  const sendNotification = async (title: string, body: string) => {
    await Notifications.scheduleNotificationAsync({
      content: { title, body },
      trigger: null,
    });
  };

  // Automatic climate control for temperature alerts
  useEffect(() => {
    if (isTempAlert && climOn === false && !hasAppliedTempAlert.current) {
      hasAppliedTempAlert.current = true;
      toggleClimat(true);
    }
  }, [isTempAlert, climOn]);

  // Automatic light control for night mode - only run once per mount
  useEffect(() => {
    if (lightOn === null) return; // Wait for initial state to load
    
    if (isNightMode && lightOn && !hasAppliedNightMode.current) {
      hasAppliedNightMode.current = true;
      toggleLight();
    } else if (!isNightMode && !lightOn && !hasAppliedNightMode.current) {
      hasAppliedNightMode.current = true;
      toggleLight();
    }
  }, [isNightMode, lightOn]);

  const chartConfig = {
    backgroundColor: "#fff",
    backgroundGradientFrom: "#fff",
    backgroundGradientTo: "#fff",
    decimalPlaces: 0,
    color: () => "#C8A27C",
    labelColor: () => "#777",
  };

  return (
    <ScrollView 
      style={styles.container}
      refreshControl={
        <RefreshControl
          refreshing={refreshing}
          onRefresh={onRefresh}
          tintColor="#C8A27C"
          colors={["#C8A27C"]}
        />
      }
    >
      <Text style={styles.title}>Historique – {id}</Text>

      {isTempAlert && (
        <View style={styles.alertWarning}>
          <Text>⚠️ Température élevée détectée</Text>
        </View>
      )}

      <View style={styles.mainCard}>
        <Text style={styles.sectionTitle}>
          Actions automatiques & manuelles
        </Text>

        {/* 🌡️ CLIMAT */}
        <View style={styles.climatCard}>
          <View style={styles.rowBetween}>
            <Text style={styles.cardTitle}>🌡️ Climat</Text>
            {climOn === null ? (
              <ActivityIndicator size="small" color="#C8A27C" />
            ) : (
              <Switch 
                value={climOn} 
                onValueChange={toggleClimat}
              />
            )}
          </View>

          <View style={styles.tempControl}>
            <TouchableOpacity 
              onPress={() => handleTempChange(-1)}
              disabled={targetTemp === null}
            >
              <Text style={styles.tempBtn}>−</Text>
            </TouchableOpacity>

            {targetTemp === null ? (
              <ActivityIndicator size="small" color="#C8A27C" />
            ) : (
              <Text style={styles.tempValue}>{targetTemp}°</Text>
            )}

            <TouchableOpacity 
              onPress={() => handleTempChange(1)}
              disabled={targetTemp === null}
            >
              <Text style={styles.tempBtn}>+</Text>
            </TouchableOpacity>
          </View>

          <View style={styles.rowBetween}>
            <Text style={styles.smallText}>
              ACTUEL {currentTemp !== null ? `${currentTemp.toFixed(1)}°C` : '---'}
            </Text>
            <Text style={styles.smallText}>
              STATUS {climOn ? "ACTIVE" : "OFF"}
            </Text>
          </View>
        </View>

        {/* 💡 LUMIERE */}
        <View style={styles.simpleCard}>
          <View style={styles.rowBetween}>
            <Text style={styles.cardTitle}>💡 Lumière</Text>

            {lightOn === null ? (
              <ActivityIndicator size="small" color="#C8A27C" />
            ) : (
              <TouchableOpacity
                style={[
                  styles.controlBtn,
                  { backgroundColor: lightOn ? "#6E5B4A" : "#3C3C3C" }
                ]}
                onPress={toggleLight}
                activeOpacity={0.7}
              >
                <Text style={{color:"#fff"}}>
                  {lightOn ? "ON" : "OFF"}
                </Text>
              </TouchableOpacity>
            )}
          </View>

          <Text style={styles.roomLabel}>{id}</Text>
        </View>

        {/* 🪟 FENETRES */}
        <View style={styles.simpleCard}>
          <View style={styles.rowBetween}>
            <Text style={styles.cardTitle}>🪟 Fenêtres</Text>

            {windowOpen === null ? (
              <ActivityIndicator size="small" color="#C8A27C" />
            ) : (
              <TouchableOpacity
                style={[
                  styles.controlBtn,
                  { backgroundColor: windowOpen ? "#6E5B4A" : "#3C3C3C" }
                ]}
                onPress={toggleWindow}
                activeOpacity={0.7}
              >
                <Text style={{color:"#fff"}}>
                  {windowOpen ? "OPEN" : "CLOSED"}
                </Text>
              </TouchableOpacity>
            )}
          </View>

          <Text style={styles.roomLabel}>{id}</Text>
        </View>
      </View>

      {/* CHARTS */}
      <Text style={styles.subtitle}>Température (°C)</Text>
      {temperatureData.length > 0 && labels.length > 0 ? (
        <LineChart
          data={{
            labels: labels,
            datasets: [{ data: temperatureData }],
          }}
          width={screenWidth - 40}
          height={220}
          chartConfig={chartConfig}
          style={styles.chart}
        />
      ) : (
        <View style={styles.chart}>
          <Text style={{ textAlign: 'center', padding: 20 }}>No data available</Text>
        </View>
      )}

      <Text style={styles.subtitle}>Humidité (%)</Text>
      {humidityData.length > 0 && labels.length > 0 ? (
        <LineChart
          data={{
            labels: labels,
            datasets: [{ data: humidityData }],
          }}
          width={screenWidth - 40}
          height={220}
          chartConfig={chartConfig}
          style={styles.chart}
        />
      ) : (
        <View style={styles.chart}>
          <Text style={{ textAlign: 'center', padding: 20 }}>No data available</Text>
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container:{
    flex:1,
    backgroundColor:"#F2EFEC",
    padding:16
  },

  title:{
    fontSize:22,
    fontWeight:"600",
    marginBottom:12
  },

  mainCard:{
    backgroundColor:"#FFFFFF",
    borderRadius:20,
    padding:16
  },

  sectionTitle:{
    fontWeight:"600",
    marginBottom:12
  },

  climatCard:{
    backgroundColor:"#B89C80",
    borderRadius:20,
    padding:16,
    marginBottom:16
  },

  subCard:{
    backgroundColor:"#B89C80",
    borderRadius:20,
    padding:16,
    marginBottom:16
  },

  cardTitle:{
    color:"#fff",
    fontSize:16,
    fontWeight:"600"
  },

  rowBetween:{
    flexDirection:"row",
    justifyContent:"space-between",
    alignItems:"center"
  },

  tempControl:{
    flexDirection:"row",
    justifyContent:"center",
    alignItems:"center",
    marginVertical:20
  },

  tempBtn:{
    fontSize:28,
    color:"#fff",
    marginHorizontal:20
  },

  tempValue:{
    fontSize:36,
    fontWeight:"700",
    color:"#fff"
  },

  smallText:{
    color:"#fff"
  },

  roomRow:{
    flexDirection:"row",
    justifyContent:"space-between",
    marginTop:12,
    alignItems:"center"
  },

  windowRow:{
    flexDirection:"row",
    justifyContent:"space-between",
    marginTop:12,
    alignItems:"center",
    backgroundColor:"#A88C72",
    padding:12,
    borderRadius:14
  },

  roomText:{
    color:"#fff",
    fontSize:16
  },

  offBtn:{
    backgroundColor:"#6E5B4A",
    paddingVertical:6,
    paddingHorizontal:14,
    borderRadius:14
  },

  iconBtn:{
    backgroundColor:"#6E5B4A",
    padding:10,
    borderRadius:12,
    marginLeft:8
  },

  link:{
    color:"#E5E5FF"
  },

  alertWarning:{
    backgroundColor:"#F5E3B0",
    padding:10,
    borderRadius:14,
    marginBottom:8
  },

  alertDanger:{
    backgroundColor:"#F3C5C5",
    padding:10,
    borderRadius:14,
    marginBottom:8
  },
 
  simpleCard:{
    backgroundColor:"#B89C80",
    borderRadius:20,
    padding:16,
    marginBottom:16
  },

  controlBtn:{
    backgroundColor:"#6E5B4A",
    paddingVertical:8,
    paddingHorizontal:18,
    borderRadius:20
  },

  roomLabel:{
    color:"#fff",
    marginTop:8,
    fontSize:14
},

  subtitle:{
    fontSize:18,
    fontWeight:"600",
    marginTop:20,
    marginBottom:12
  },

  chart:{
    backgroundColor:"#fff",
    borderRadius:20,
    marginBottom:20,
    overflow:"hidden"
  }
});