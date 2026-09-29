// Copyright 2026 Sriram
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <gtest/gtest.h>
#include <fstream>
#include <iterator>
#include <string>
#include <vector>
#include <cstdlib>
#include <filesystem>

namespace fs = std::filesystem;

// Resolves share/drone_description from AMENT_PREFIX_PATH (or COLCON fallback)
static fs::path packageShare() {
    const char* prefixes = std::getenv("AMENT_PREFIX_PATH");
    if (prefixes) {
        std::string pfx{prefixes};
        std::size_t start = 0;
        while (start <= pfx.size()) {
            std::size_t end = pfx.find(':', start);
            fs::path cand = fs::path(pfx.substr(start, end - start)) /
                            "share" / "drone_description";
            if (fs::exists(cand)) return cand;
            if (end == std::string::npos) break;
            start = end + 1;
        }
    }
    return fs::path{};
}

class DroneDescriptionTest : public ::testing::Test {
protected:
    fs::path package_path;
    fs::path urdf_path;

    void SetUp() override {
        package_path = packageShare();
        urdf_path = package_path / "urdf" / "drone.xacro";
    }

    static std::string readFile(const fs::path& p) {
        std::ifstream file(p);
        EXPECT_TRUE(file.is_open()) << "Cannot open " << p;
        return std::string((std::istreambuf_iterator<char>(file)),
                           std::istreambuf_iterator<char>());
    }
};

TEST_F(DroneDescriptionTest, PackageExists) {
    ASSERT_FALSE(package_path.empty())
        << "drone_description share dir not found in AMENT_PREFIX_PATH";
}

TEST_F(DroneDescriptionTest, MainXacroExists) {
    EXPECT_TRUE(fs::exists(urdf_path)) << "Main xacro not found: " << urdf_path;
}

TEST_F(DroneDescriptionTest, SensorMacrosExist) {
    EXPECT_TRUE(fs::exists(package_path / "urdf" / "macros" / "sensors.xacro"));
    EXPECT_TRUE(fs::exists(package_path / "urdf" / "macros" / "gimbal.xacro"));
    EXPECT_TRUE(fs::exists(package_path / "urdf" / "macros" / "px4.xacro"));
}

TEST_F(DroneDescriptionTest, XacroSyntaxValid) {
    std::string content = readFile(urdf_path);
    ASSERT_FALSE(content.empty());

    EXPECT_NE(content.find("<robot"), std::string::npos) << "Missing robot root";
    EXPECT_NE(content.find("xmlns:xacro"), std::string::npos) << "Missing xacro ns";
    EXPECT_NE(content.find("name=\"f450_drone\""), std::string::npos);

    // Macro includes
    EXPECT_NE(content.find("sensors.xacro"), std::string::npos);
    EXPECT_NE(content.find("gimbal.xacro"), std::string::npos);
    EXPECT_NE(content.find("px4.xacro"), std::string::npos);

    // Sensor macro instantiations
    EXPECT_NE(content.find("downward_1d_lidar"), std::string::npos);
    EXPECT_NE(content.find("downward_optical_flow"), std::string::npos);
    EXPECT_NE(content.find("forward_camera_45deg"), std::string::npos);
    EXPECT_NE(content.find("gimbal_assembly"), std::string::npos);
    EXPECT_NE(content.find("gz_imu_sensor"), std::string::npos);
    EXPECT_NE(content.find("pixhawk4_flight_stack"), std::string::npos);
}

TEST_F(DroneDescriptionTest, SensorMacrosContent) {
    auto check_macro = [&](const std::string& macro_file,
                           const std::vector<std::string>& required) {
        std::string content = readFile(package_path / "urdf" / "macros" / macro_file);
        ASSERT_FALSE(content.empty()) << "Could not open " << macro_file;
        for (const auto& req : required) {
            EXPECT_NE(content.find(req), std::string::npos)
                << "Missing '" << req << "' in " << macro_file;
        }
    };

    check_macro("sensors.xacro", {
        "downward_1d_lidar",
        "downward_optical_flow",
        "forward_camera_45deg",
        "gimbal_2d_lidar",
        "gz_imu_sensor",
        "type=\"gpu_lidar\"",   // gz-sim 10 ray sensor
        "type=\"camera\"",
        "type=\"imu\"",
    });

    check_macro("gimbal.xacro", {
        "gimbal_assembly",
        "continuous",                                  // yaw joint type
        "${name}_yaw_joint",                           // joint name template
        "gz-sim-joint-position-controller-system",     // real gz plugin
        "gz-sim-joint-state-publisher-system",
    });

    check_macro("px4.xacro", {
        "px4_multicopter_base",
        "pixhawk4_flight_stack",
        "pixhawk4_motor",
        "gz-sim-multicopter-control-system",           // velocity controller
        "gz-sim-multicopter-motor-model-system",       // per-rotor thrust
        "gz-sim-odometry-publisher-system",            // ground truth
        "rotorConfiguration",
    });
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
