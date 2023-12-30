# Verify_Me
#### Video Demo: https://youtu.be/Uv_689hzC-I
#### Description:
verify_me is an innovative app designed for my CS50P class, offering a secure and private way for users to verify their identity for various services. By generating IDs which can be used by the service provider to verify the person in front of them, verify_me enables verification without physical documents, and protects user privacy by providing only information a service provider requires and not one bit more.

## Technical Overview

### In-Memory Database
- Uses an in-memory SQLite database as a placeholder for a more robust, scalable solution in a production environment. A real cache that utilizes TTL for expiration.

### Scalable Backend Architecture
- Ideal for cloud hosting, functions are parallelizable for scalability and speed.

### Future Enhancements (Not Yet Implemented)
- Verification Expiration and One-Time-Use IDs.
- User and Service Provider Interfaces.
- Data synchronization with official records.
- Security.

## Usage Scenarios

### Flight Verification
- Users only need to provide their name and photo.
- The system cross-references this information with the boarding pass and stored data, ensuring accurate verification without unnecessary data exposure.

### Bar Entry
- Simplifies verification to just a photo and legal drinking age confirmation.
- Eliminates the need to share sensitive information like name or exact date of birth.

## Current Limitations and Challenges
- Requires device and internet access. This excludes people that can't purchase a device, or can't afford expensive data plans, especially in Canada.
- Dependent on governmental and official recognition for sensitive verifications. In order for verify_me to work as a passport, airlines have to be able to trust it, which can only happen with government certification of the underlying data.
- Centralization of data, which can be dangerous if security is not handled well.

## Conclusion
`verify_me` is a solution digital identity verification, focusing on privacy, security, and user convenience to replace the dinosaur-era hassle of physical documents.
