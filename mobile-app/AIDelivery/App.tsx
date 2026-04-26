import React, { useState } from 'react';
import { Alert } from 'react-native';
import {
  View,
  Text,
  TextInput,
  Button,
  StyleSheet,
} from 'react-native';

export default function App() {
  const [mode, setMode] = useState<string>("");
  const [status, setStatus] = useState<string>("");
  const [question, setQuestion] = useState<string>("");
  const [response, setResponse] = useState<string>("");

  // 🚗 Driver API
  const updateStatus = async () => {
    await fetch("http://10.0.2.2:8000/update-driver-status", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        order_id: "123",
        status: status,
        lat: -33.8688,
        lng: 151.2093,
      }),
    });

    Alert.alert("Success", "Status updated!");
    setStatus("");
  };

  // 👤 Customer API
  const askAI = async () => {
    const res = await fetch("http://10.0.2.2:8000/ask-ai", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        order_id: "123",
        question: question,
      }),
    });

    const data = await res.json();
    setResponse(data.ai_response);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>AI Delivery Assistant</Text>

      {/* Main Screen */}
      {!mode && (
        <View>
          <Button title="Driver" onPress={() => setMode("driver")} />
          <View style={{ marginTop: 10 }} />
          <Button title="Customer" onPress={() => setMode("customer")} />
        </View>
      )}

      {/* Driver Panel */}
      {mode === "driver" && (
        <View>
          <Button title="Back" onPress={() => setMode("")} />
          <Text style={styles.subtitle}>Driver Panel</Text>

          <TextInput
            style={styles.input}
            placeholder="Enter status"
            value={status}
            onChangeText={setStatus}
          />

          <Button title="Update Status" onPress={updateStatus} />
        </View>
      )}

      {/* Customer Panel */}
      {mode === "customer" && (
        <View>
          <Button title="Back" onPress={() => setMode("")} />
          <Text style={styles.subtitle}>Customer Panel</Text>

          <TextInput
            style={styles.input}
            placeholder="Ask about your order"
            value={question}
            onChangeText={setQuestion}
          />

          <Button title="Ask" onPress={askAI} />

          {response !== "" && (
            <Text style={styles.response}>Response: {response}</Text>
          )}
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: 'center',
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 18,
    marginVertical: 10,
  },
  input: {
    borderWidth: 1,
    padding: 10,
    marginVertical: 10,
    borderRadius: 5,
  },
  response: {
    marginTop: 15,
    fontSize: 16,
  },
});