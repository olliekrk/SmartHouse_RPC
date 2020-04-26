import com.zeroc.Ice.Util;
import locators.HouseServantLocator;
import lombok.extern.slf4j.Slf4j;
import servants.home.HomeStatusI;

import java.util.Arrays;

@Slf4j
public class HouseServer {
    private static final String HOUSE_ADAPTER_NAME = "HouseAdapter";

    public static void main(String[] args) {
        log.info("Starting the server.");
        try (var communicator = Util.initialize(args)) {
            Runtime.getRuntime().addShutdownHook(new Thread(communicator::destroy));
            log.info("Startup successful.");
            launch(communicator);
        }
        log.info("Server was shut down.");
    }

    private static void launch(com.zeroc.Ice.Communicator communicator) {
        var adapter = communicator.createObjectAdapter(HOUSE_ADAPTER_NAME);

        var locator = new HouseServantLocator();
        var categories = new String[]{"wall_camera", "drone_camera", "grass_mower", "fridge", "home"};

        log.info("Assigning Servant Locator for categories: " + Arrays.toString(categories));
        Arrays.stream(categories).forEach(category -> adapter.addServantLocator(locator, category));

        log.info("Activating servant for listing active devices with ID: " + HomeStatusI.loggableIdentity(HomeStatusI.HOME_GLOBAL));
        adapter.add(new HomeStatusI(), HomeStatusI.HOME_GLOBAL);

        adapter.activate();
        log.info("Activated. Waiting for requests to serve.");

        communicator.waitForShutdown();
    }
}
