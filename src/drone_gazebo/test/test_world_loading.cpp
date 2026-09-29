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
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <iterator>
#include <string>

namespace fs = std::filesystem;

// Locate share/drone_gazebo via AMENT_PREFIX_PATH
static fs::path shareDir() {
    const char* prefixes = std::getenv("AMENT_PREFIX_PATH");
    if (prefixes) {
        std::string pfx{prefixes};
        std::size_t start = 0;
        while (start <= pfx.size()) {
            std::size_t end = pfx.find(':', start);
            fs::path cand = fs::path(pfx.substr(start, end - start)) /
                            "share" / "drone_gazebo";
            if (fs::exists(cand)) return cand;
            if (end == std::string::npos) break;
            start = end + 1;
        }
    }
    return fs::path{};
}

TEST(WorldLoading, HouseWorldExists) {
    fs::path share = shareDir();
    ASSERT_FALSE(share.empty()) << "drone_gazebo share not found";
    fs::path world = share / "worlds" / "house_indoor.sdf";
    EXPECT_TRUE(fs::exists(world)) << "Missing world: " << world;
}

TEST(WorldLoading, HouseWorldHasRequiredSystems) {
    fs::path world = shareDir() / "worlds" / "house_indoor.sdf";
    std::ifstream file(world);
    ASSERT_TRUE(file.is_open());
    std::string content((std::istreambuf_iterator<char>(file)),
                        std::istreambuf_iterator<char>());

    // gz-sim 10 world system plugins
    EXPECT_NE(content.find("gz-sim-physics-system"), std::string::npos);
    EXPECT_NE(content.find("gz-sim-sensors-system"), std::string::npos);
    EXPECT_NE(content.find("gz-sim-imu-system"), std::string::npos);
    // House content: walls + furniture
    EXPECT_NE(content.find("<sdf"), std::string::npos);
    EXPECT_NE(content.find("wall_north"), std::string::npos);
    EXPECT_NE(content.find("sofa"), std::string::npos);
}

TEST(WorldLoading, BridgeConfigExists) {
    fs::path cfg = shareDir() / "config" / "bridge.yaml";
    EXPECT_TRUE(fs::exists(cfg)) << "Missing bridge config: " << cfg;
}
