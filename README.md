# 🚶‍♂️ Walking Process

Welcome to the **Walking Process** – your personal activity tracker that transforms every step you take into rewarding WON! This application leverages real-time geolocation data to accurately calculate your steps and incentivizes physical activity with a unique rewards system. Read on for an in-depth explanation of how the walking process works, the underlying mechanics of the reward system, and how these rewards might evolve over time.

---

## 📡 How the Walking Process Works

### 1. **Session Initiation**  
- **Initial Setup:**  
  The application initializes a temporary session containing:  
  - **User ID:** For session identification.  
  - **commit Counter:** Set to zero at the beginning.  
  - **Session Timestamp:** Indicates when the session starts.  
  - **No tracking or server storage:** Data is processed only during the session.  


### 2. **Real-Time Step Calculation**
- **Geolocation Updates:**  
  As you walk, your device periodically sends updated geolocation data to Telegram. Telegram processes this data, while the application calculates the distance traveled.
- **Step Estimation:**  
Based on an approximate average of 0.8 meters per step (the average stride length of an adult human), the distance is converted into a step count.
- **Message Updates:**  
  The application continuously updates a status message showing your total step count during the session.

### 3. **Session Management**
- **Active Monitoring:**  
  The application monitors your session actively. If no significant movement is detected for a defined period, the session automatically ends to prevent abuse.
- **Cheating Prevention:**  
  A built-in check compares the number of steps calculated over each interval with a maximum threshold (set to 111 steps per 15 sec interval). If the step count exceeds this threshold, the application warns you about walking too fast, which could indicate potential cheating.
- **Session Termination:**  
  You can stop the session manually by issuing a stop command, or the session will end automatically if prolonged inactivity is detected. Upon termination, the application sends a summary of your activity.

---

## 💰 The Rewards System

### **Base Rewards**
- **Fixed Reward:**  
  For every 100 steps taken, you earn **15 WON**. This is defined as the base reward in the system.
  
### **Future Reward Components**
While the current implementation only uses the base reward, future updates will introduce halving processes that gradually reduce the reward amount:
- **LISTING:** 7.5 WON 
- **HALVING:** 3.25 WON  
- **MINING:** 1.625 WON 


### **Dynamic Reward Evolution**
- **Potential Adjustments:**  
  As the system evolves, future updates might modify reward coefficients. For instance, during peak activity periods or special events, rewards could be increased temporarily to boost motivation.
- **Incentive Tiers:**  
  Future versions may introduce a tiered rewards mechanism where prolonged or high-intensity walking sessions could unlock bonus multipliers.
- **Adaptive Rewards:**  
  The reward system is designed to be flexible, allowing adjustments based on overall user engagement and additional parameters, ensuring that the rewards remain fair and motivating over time.

---

## 🔧 Technical Overview & Architecture

- **Session Data Handling:**  
  Integrated with the Telegram API (via libraries like aiogram), the application handles commands, sends real-time messages, and updates status notifications seamlessly.
- **Scalability:**  
  Designed with modularity in mind, the code architecture supports future extensions, including advanced reward dynamics, additional anti-cheat measures, and integration with other services like smart watch.

---

## 🔒 Security & Privacy

Our commitment to your privacy and data security is paramount. The Walking Process application is designed with a security-first approach, ensuring that no personal data is collected or stored. Here’s how we ensure your data remains safe:

- **Minimal Data Access:**  
  The application only accesses the geolocation data necessary to calculate the number of steps taken during each interval. No additional personal information is requested or recorded.
- **Ephemeral Data Handling:**  
  All geolocation data is processed in real time solely for the purpose of computing step counts. Once the calculation is complete, the data is immediately discarded and not stored in any persistent database.
- **No User Tracking:**  
  We do not track, log, or store any details about your location history, personal identity, or any other sensitive information. The application only captures the metric of your step count during active sessions.
- **Security by Design:**  
  The system is architected to limit data flows strictly to what is necessary for functionality. Temporary in-memory storage is used for session data, which is purged once the session concludes.
- **User Control and Transparency:**  
  You remain in full control of your data. The application only uses data that you explicitly provide during a session, and there is no sharing of this data with third parties. Every operation involving your data is transparent, with clear statements on what is accessed and why.
- **Regular Security Audits:**  
  We continuously review and update our security measures to ensure compliance with best practices and to safeguard against emerging vulnerabilities.
- **No Data Persistence:**  
  Importantly, the application does not store any geolocation or personal data beyond the immediate calculation of your steps. This ensures that your privacy is maintained at all times, and no user-specific data is retained after a session ends.

---

## 🌟 Final Thoughts

The **Walking Process** is more than just a fitness tracker; it’s a platform designed to motivate and reward healthy living. By converting every step into tangible rewards, it creates a fun and engaging way to stay active. With a robust, adaptable reward system and a modular design, this application is poised to evolve with your needs and the latest trends in fitness technology.

Let’s take every step together towards a healthier, more rewarding lifestyle!💰 🏃‍♂️

---

*Happy Walking!*
