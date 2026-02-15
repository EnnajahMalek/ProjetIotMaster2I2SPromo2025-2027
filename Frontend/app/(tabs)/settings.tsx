import { useCallback, useContext, useEffect, useMemo, useState } from "react";
import {
  Alert,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Switch,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { useRouter } from "expo-router";
import { Ionicons } from "@expo/vector-icons";
import AsyncStorage from "@react-native-async-storage/async-storage";
import * as Notifications from "expo-notifications";
import { AuthContext } from "../../context/AuthContext";

const STORAGE_KEYS = {
  notifications: "settings_notifications_enabled",
  darkMode: "settings_dark_mode_enabled",
  autoRefresh: "settings_auto_refresh_enabled",
};

export default function Settings() {
  const router = useRouter();
  const { logout } = useContext(AuthContext);

  const [notificationsEnabled, setNotificationsEnabled] = useState(true);
  const [darkModeEnabled, setDarkModeEnabled] = useState(false);
  const [autoRefreshEnabled, setAutoRefreshEnabled] = useState(true);
  const [isLoading, setIsLoading] = useState(true);

  const theme = useMemo(
    () =>
      darkModeEnabled
        ? {
            background: "#1F1F1F",
            card: "#2B2B2B",
            title: "#F2EFEC",
            text: "#E5DDD5",
            muted: "#B8B0A8",
            accent: "#C8A27C",
            border: "#3B3B3B",
          }
        : {
            background: "#EFEAE6",
            card: "#FFFFFF",
            title: "#1F1F1F",
            text: "#3A3A3A",
            muted: "#7D746B",
            accent: "#C8A27C",
            border: "#E8E0D8",
          },
    [darkModeEnabled]
  );

  const saveSetting = useCallback(async (key: string, value: boolean) => {
    try {
      await AsyncStorage.setItem(key, value ? "1" : "0");
    } catch (error) {
      console.log("Settings save error:", error);
    }
  }, []);

  useEffect(() => {
    const loadSettings = async () => {
      try {
        const [notifValue, darkValue, refreshValue] = await Promise.all([
          AsyncStorage.getItem(STORAGE_KEYS.notifications),
          AsyncStorage.getItem(STORAGE_KEYS.darkMode),
          AsyncStorage.getItem(STORAGE_KEYS.autoRefresh),
        ]);

        if (notifValue !== null) setNotificationsEnabled(notifValue === "1");
        if (darkValue !== null) setDarkModeEnabled(darkValue === "1");
        if (refreshValue !== null) setAutoRefreshEnabled(refreshValue === "1");
      } catch (error) {
        console.log("Settings load error:", error);
      } finally {
        setIsLoading(false);
      }
    };

    loadSettings();
  }, []);

  const onNotificationsToggle = useCallback(
    async (value: boolean) => {
      if (value) {
        const { status } = await Notifications.requestPermissionsAsync();
        if (status !== "granted") {
          Alert.alert(
            "Permission requise",
            "Les notifications sont bloquees. Active-les dans les reglages du telephone."
          );
          setNotificationsEnabled(false);
          await saveSetting(STORAGE_KEYS.notifications, false);
          return;
        }
      }

      setNotificationsEnabled(value);
      await saveSetting(STORAGE_KEYS.notifications, value);
    },
    [saveSetting]
  );

  const onDarkModeToggle = useCallback(
    async (value: boolean) => {
      setDarkModeEnabled(value);
      await saveSetting(STORAGE_KEYS.darkMode, value);
    },
    [saveSetting]
  );

  const onAutoRefreshToggle = useCallback(
    async (value: boolean) => {
      setAutoRefreshEnabled(value);
      await saveSetting(STORAGE_KEYS.autoRefresh, value);
    },
    [saveSetting]
  );

  const handleLogout = useCallback(() => {
    Alert.alert("Deconnexion", "Voulez-vous vous deconnecter ?", [
      { text: "Annuler", style: "cancel" },
      {
        text: "Deconnexion",
        style: "destructive",
        onPress: async () => {
          try {
            await AsyncStorage.removeItem("authToken");
          } catch (error) {
            console.log("Token clear error:", error);
          }
          logout?.();
          router.replace("/auth/login");
        },
      },
    ]);
  }, [logout, router]);

  return (
    <SafeAreaView style={[styles.safeArea, { backgroundColor: theme.background }]}>
      <ScrollView
        style={[styles.container, { backgroundColor: theme.background }]}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.header}>
          <Text style={[styles.title, { color: theme.title }]}>Settings</Text>
          <Text style={[styles.subtitle, { color: theme.muted }]}>
            Gere ton application IoT Smart Home
          </Text>
        </View>

        <View style={[styles.card, { backgroundColor: theme.card, borderColor: theme.border }]}>
          <SettingRow
            icon="notifications-outline"
            title="Notifications"
            description="Recevoir les alertes capteurs et securite"
            value={notificationsEnabled}
            onValueChange={onNotificationsToggle}
            accent={theme.accent}
            text={theme.text}
            muted={theme.muted}
            disabled={isLoading}
          />
          <Separator color={theme.border} />
          <SettingRow
            icon="moon-outline"
            title="Mode sombre"
            description="Activer un affichage sombre dans cette page"
            value={darkModeEnabled}
            onValueChange={onDarkModeToggle}
            accent={theme.accent}
            text={theme.text}
            muted={theme.muted}
            disabled={isLoading}
          />
          <Separator color={theme.border} />
          <SettingRow
            icon="refresh-outline"
            title="Auto refresh"
            description="Rafraichissement automatique des donnees"
            value={autoRefreshEnabled}
            onValueChange={onAutoRefreshToggle}
            accent={theme.accent}
            text={theme.text}
            muted={theme.muted}
            disabled={isLoading}
          />
        </View>

        <View style={[styles.card, { backgroundColor: theme.card, borderColor: theme.border }]}>
          <ActionRow
            icon="person-outline"
            label="Mon profil"
            color={theme.text}
            onPress={() => router.push("/profile")}
          />
          <Separator color={theme.border} />
          <ActionRow
            icon="log-out-outline"
            label="Deconnexion"
            color="#C05B52"
            onPress={handleLogout}
          />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

function SettingRow({
  icon,
  title,
  description,
  value,
  onValueChange,
  accent,
  text,
  muted,
  disabled,
}: {
  icon: keyof typeof Ionicons.glyphMap;
  title: string;
  description: string;
  value: boolean;
  onValueChange: (value: boolean) => void;
  accent: string;
  text: string;
  muted: string;
  disabled?: boolean;
}) {
  return (
    <View style={styles.settingRow}>
      <View style={[styles.iconWrap, { backgroundColor: accent }]}>
        <Ionicons name={icon} size={18} color="#FFFFFF" />
      </View>
      <View style={styles.settingTextWrap}>
        <Text style={[styles.settingTitle, { color: text }]}>{title}</Text>
        <Text style={[styles.settingDesc, { color: muted }]}>{description}</Text>
      </View>
      <Switch value={value} onValueChange={onValueChange} disabled={disabled} />
    </View>
  );
}

function ActionRow({
  icon,
  label,
  color,
  onPress,
}: {
  icon: keyof typeof Ionicons.glyphMap;
  label: string;
  color: string;
  onPress: () => void;
}) {
  return (
    <TouchableOpacity style={styles.actionRow} onPress={onPress} activeOpacity={0.8}>
      <Ionicons name={icon} size={20} color={color} />
      <Text style={[styles.actionText, { color }]}>{label}</Text>
      <Ionicons name="chevron-forward" size={18} color={color} />
    </TouchableOpacity>
  );
}

function Separator({ color }: { color: string }) {
  return <View style={[styles.separator, { backgroundColor: color }]} />;
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
  },
  container: {
    flex: 1,
  },
  content: {
    paddingHorizontal: 20,
    paddingTop: 18,
    paddingBottom: 28,
  },
  header: {
    marginBottom: 18,
  },
  title: {
    fontSize: 28,
    fontWeight: "700",
  },
  subtitle: {
    marginTop: 6,
    fontSize: 14,
  },
  card: {
    borderRadius: 20,
    borderWidth: 1,
    paddingVertical: 8,
    paddingHorizontal: 14,
    marginBottom: 16,
  },
  settingRow: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: 12,
  },
  iconWrap: {
    width: 34,
    height: 34,
    borderRadius: 10,
    alignItems: "center",
    justifyContent: "center",
  },
  settingTextWrap: {
    flex: 1,
    marginLeft: 10,
    marginRight: 8,
  },
  settingTitle: {
    fontSize: 16,
    fontWeight: "600",
  },
  settingDesc: {
    marginTop: 2,
    fontSize: 12,
  },
  actionRow: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: 14,
  },
  actionText: {
    flex: 1,
    marginLeft: 10,
    fontSize: 15,
    fontWeight: "600",
  },
  separator: {
    height: 1,
    opacity: 0.8,
  },
});
