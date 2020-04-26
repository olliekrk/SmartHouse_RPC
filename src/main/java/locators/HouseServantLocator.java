package locators;

import com.zeroc.Ice.ServantLocator;
import servants.home.HomeStatusI;
import servants.home.garden.DroneCameraControllerI;
import servants.home.garden.GrassMowerControllerI;
import servants.home.garden.WallCameraControllerI;
import servants.home.kitchen.FridgeControllerI;

public class HouseServantLocator implements ServantLocator {

    @Override
    public ServantLocator.LocateResult locate(com.zeroc.Ice.Current current) {
        if (current.id.category.equals("home")) {
            return new LocateResult(findHomeStatusI(current), null);
        }

        var controller = createController(current.id.category);
        if (controller != null) {
            findHomeStatusI(current).register(current.id);
            current.adapter.add(controller, current.id); // adds to ASM
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

    private com.zeroc.Ice.Object createController(String category) {
        switch (category) {
            case "wall_camera":
                return new WallCameraControllerI();
            case "drone_camera":
                return new DroneCameraControllerI();
            case "grass_mower":
                return new GrassMowerControllerI();
            case "fridge":
                return new FridgeControllerI();
            case "home":
                return new HomeStatusI();
            default:
                return null;
        }
    }
}
