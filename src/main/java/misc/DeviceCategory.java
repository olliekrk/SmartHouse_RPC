package misc;

import java.util.Arrays;

public enum DeviceCategory {
    HOME("home"),
    GRASS_MOWER("grass_mower"),
    FRIDGE("fridge"),
    DRONE_CAMERA("drone_camera"),
    WALL_CAMERA("wall_camera");

    private final String name;

    DeviceCategory(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public static String[] names() {
        return Arrays.stream(DeviceCategory.values()).map(DeviceCategory::getName).toArray(String[]::new);
    }
}
