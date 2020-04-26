package locators;

import com.zeroc.Ice.ServantLocator;
import misc.DeviceCategory;
import servants.home.HomeStatusI;
import servants.home.garden.DroneCameraControllerI;
import servants.home.garden.GrassMowerControllerI;
import servants.home.garden.WallCameraControllerI;
import servants.home.kitchen.FridgeControllerI;

public class HouseServantLocator implements ServantLocator {

    @Override
    public ServantLocator.LocateResult locate(com.zeroc.Ice.Current current) {
        if (current.id.category.equals(DeviceCategory.HOME.getName())) {
            return new LocateResult(findHomeStatusI(current), null);
        }

        var controller = createController(current.id.category);
        if (controller != null) {
            findHomeStatusI(current).register(current.id);
            current.adapter.add(controller, current.id); // add to ASM
        }

        return new LocateResult(controller, null);
    }

    @Override
    public void finished(com.zeroc.Ice.Current current, com.zeroc.Ice.Object servant, java.lang.Object cookie) {
    }

    @Override
    public void deactivate(String category) {
    }

    private HomeStatusI findHomeStatusI(com.zeroc.Ice.Current current) {
        return (HomeStatusI) current.adapter.find(HomeStatusI.HOME_GLOBAL);
    }

    private com.zeroc.Ice.Object createController(String categoryName) {
        if (categoryName.equals(DeviceCategory.WALL_CAMERA.getName())) return new WallCameraControllerI();
        else if (categoryName.equals(DeviceCategory.DRONE_CAMERA.getName())) return new DroneCameraControllerI();
        else if (categoryName.equals(DeviceCategory.GRASS_MOWER.getName())) return new GrassMowerControllerI();
        else if (categoryName.equals(DeviceCategory.FRIDGE.getName())) return new FridgeControllerI();
        else if (categoryName.equals(DeviceCategory.HOME.getName())) return new HomeStatusI();
        else return null;
    }
}
