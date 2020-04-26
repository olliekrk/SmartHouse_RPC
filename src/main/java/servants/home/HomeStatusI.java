package servants.home;

import Home.HomeStatus;
import com.zeroc.Ice.Current;
import com.zeroc.Ice.Identity;

import java.util.concurrent.ConcurrentLinkedDeque;

public class HomeStatusI implements HomeStatus {

    public static final Identity HOME_GLOBAL = new Identity("global", "home");

    private final ConcurrentLinkedDeque<Identity> objectIdentities;

    public HomeStatusI() {
        objectIdentities = new ConcurrentLinkedDeque<>();
        objectIdentities.add(HOME_GLOBAL);
    }

    @Override
    public String[] getActiveDevices(Current current) {
        return objectIdentities.stream().map(HomeStatusI::loggableIdentity).toArray(String[]::new);
    }

    public void register(Identity id) {
        objectIdentities.push(id);
    }

    public static String loggableIdentity(Identity id) {
        return String.format("%s/%s", id.category, id.name);
    }

}
