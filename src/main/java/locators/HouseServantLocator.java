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
        findHomeStatusI(current).register(current.id);
        switch (current.id.category) {
            case "wall_camera":
                return new LocateResult(new WallCameraControllerI(), null);
            case "drone_camera":
                return new LocateResult(new DroneCameraControllerI(), null);
            case "grass_mower":
                return new LocateResult(new GrassMowerControllerI(), null);
            case "fridge":
                return new LocateResult(new FridgeControllerI(), null);
            case "home":
                return new LocateResult(new HomeStatusI(), null);
            default:
                return new ServantLocator.LocateResult();
        }
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

}
