# React Native Refreshers

Comprehensive React Native guide from basics to upper-mid level.
Build native mobile apps for iOS and Android using React.

## 📚 Topics Covered

### Fundamentals 📝
- **00_setup_basics.jsx** 📝 - Setup, Expo vs bare, project structure
- **01_core_components.jsx** 📝 - View, Text, Image, ScrollView, FlatList
- **02_styling.jsx** 📝 - StyleSheet, Flexbox, responsive design
- **03_user_input.jsx** 📝 - TextInput, Button, TouchableOpacity, Pressable

### Intermediate 📝
- **04_navigation.jsx** 📝 - React Navigation, Stack, Tab, Drawer
- **05_platform_specific.jsx** 📝 - Platform.OS, conditional code
- **06_networking.jsx** 📝 - Fetch, API calls, async storage
- **07_native_modules.jsx** 📝 - Camera, Location, Permissions, sensors
- **08_state_management.jsx** 📝 - Redux, Zustand, Context in mobile
- **09_animations.jsx** 📝 - Animated API, Reanimated, gestures
- **10_performance.jsx** 📝 - Optimization, memory, rendering
- **11_testing.jsx** 📝 - Jest, testing mobile components
- **12_deployment.jsx** 📝 - App Store, Google Play, OTA updates

### Status Legend:
- 📝 Template/outline (ready to expand)

## 🎯 Learning Path

1. **Setup & Basics** (00-03) - Get started with RN
2. **Navigation & Platform** (04-05) - App structure
3. **Native Features** (06-07) - Device capabilities
4. **Production** (08-12) - Polish and deploy

## 💡 Key Differences from Web React

### Components
| Web React | React Native |
|-----------|--------------|
| `<div>` | `<View>` |
| `<span>`, `<p>` | `<Text>` |
| `<img>` | `<Image>` |
| `<input>` | `<TextInput>` |
| `<button>` | `<Button>` or `<TouchableOpacity>` |
| `<ul>`, `<ol>` | `<FlatList>` or `<SectionList>` |
| `<a>` | Navigation functions |

### Styling
- ❌ No CSS files
- ✅ StyleSheet API (JavaScript objects)
- ✅ Flexbox (default layout)
- ❌ No CSS Grid, floats, or many CSS properties
- ✅ Platform-specific styles

### No DOM
- ❌ No `document`, `window`, DOM APIs
- ✅ Native platform APIs instead
- ✅ AsyncStorage instead of localStorage
- ✅ NetInfo instead of navigator.online

### Navigation
- ❌ No React Router
- ✅ React Navigation library
- ✅ Native navigation patterns (stack, tabs, drawer)

## 🔧 Setup Options

### Option 1: Expo (Recommended for Beginners)
```bash
npx create-expo-app MyApp
cd MyApp
npx expo start
```
- ✅ Quick setup
- ✅ No Xcode/Android Studio required
- ✅ Over-the-air updates
- ❌ Some native features limited

### Option 2: Bare React Native
```bash
npx react-native init MyApp
cd MyApp
npm run android  # or npm run ios
```
- ✅ Full control
- ✅ All native features
- ✅ Custom native modules
- ❌ Requires Xcode/Android Studio
- ❌ More complex setup

## 📱 Platform Support

- **iOS** - Requires macOS for development
- **Android** - Works on any OS
- **Web** - With react-native-web (experimental)

## 🚀 Quick Start Example

```jsx
import React from 'react';
import { View, Text, StyleSheet, Button } from 'react-native';

export default function App() {
  const [count, setCount] = React.useState(0);
  
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Count: {count}</Text>
      <Button title="Increment" onPress={() => setCount(count + 1)} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff'
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold'
  }
});
```

## 🔗 Related Topics

- See **React/** for web React patterns (most concepts transfer!)
- See **TypeScript/** for React Native with TypeScript
- Hooks work exactly the same way
