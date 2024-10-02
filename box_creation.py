import yaml
import box_sdk_gen as box

with open("players.yaml", "r") as file:
    PLAYERS = yaml.load(file, Loader=yaml.FullLoader)
START_DATE = "Sep 29"
END_DATE = "Oct 4"
CHALLENGE_DATE = "Sep 29"
TRIBAL_DATE = "Oct 4"
WEEK_NUMBER = 4
FOLDER_ID = "284575669307" # Folder_ID is the ID of the root folder for a Survivor Texas season located in the URL 


def create_folder(client, parent_id, folder_name):
    """Create a new folder under the specified parent."""
    return client.folders.create_folder(folder_name, parent_id)

def create_collaboration(client, folder_id, email):
    """Create a collaboration for the specified folder."""
    client.user_collaborations.create_collaboration(
    box.CreateCollaborationItem(
        type=box.CreateCollaborationItemTypeField.FOLDER.value, id=folder_id
    ),
    box.CreateCollaborationAccessibleBy(
        type=box.CreateCollaborationAccessibleByTypeField.USER.value, 
        login=email
    ),
    box.CreateCollaborationRole.EDITOR.value,
    notify=True,
)

def create_player_folders(client, parent_id):
    """Create folders for each player."""
    for player in PLAYERS:
        if player["eliminated"]:
            continue
        player_folder = create_folder(client, parent_id, f"{player['name']} Week {WEEK_NUMBER} ({START_DATE} - {END_DATE})")
        create_collaboration(client, player_folder.id, f"{player['eid']}@eid.utexas.edu")
        create_collaboration(client, player_folder.id, f"{player['eid']}@my.utexas.edu")
        # If the week starts when the challenge starts then there was a double shoot so we don't need a pre-challenge folder.
        if START_DATE != CHALLENGE_DATE:
            create_folder(client, player_folder, f"Week {WEEK_NUMBER} Pre-Challenge ({START_DATE} - {CHALLENGE_DATE})")
        create_folder(client, player_folder, f"Week {WEEK_NUMBER} Pre-Tribal ({CHALLENGE_DATE} - {TRIBAL_DATE})")


def create_challenge_folders(client, parent_id):
    """Create challenge-related folders."""
    challenge_folder = create_folder(client, parent_id, f"Week {WEEK_NUMBER} Challenge ({CHALLENGE_DATE})")
    create_folder(client, challenge_folder, f"Week {WEEK_NUMBER} Challenge Videos")
    create_folder(client, challenge_folder, f"Week {WEEK_NUMBER} Mat Chat")
    confessional_folder = create_folder(client, challenge_folder, f"Week {WEEK_NUMBER} Confessionals")
    # If the week starts when the challenge starts then there was a double shoot so we don't need a pre-challenge folder.
    if START_DATE != CHALLENGE_DATE:
        create_folder(client, confessional_folder, f"Week {WEEK_NUMBER} Pre-Challenge")
    create_folder(client, confessional_folder, f"Week {WEEK_NUMBER} Post-Challenge")
    create_folder(client, challenge_folder, f"Week {WEEK_NUMBER} Photographs")
    create_folder(client, challenge_folder, f"Week {WEEK_NUMBER} Miscellaneous")


def create_tribal_folders(client, parent_id):
    """Create tribal-related folders."""
    tribal_folder = create_folder(client, parent_id, f"Tribal ({TRIBAL_DATE})")
    create_folder(client, tribal_folder, f"Week {WEEK_NUMBER} Tribal Videos")
    tribal_confessionals = create_folder(client, tribal_folder, "Confessionals")
    create_folder(client, tribal_confessionals, f"Week {WEEK_NUMBER} Pre-Tribal")
    create_folder(client, tribal_confessionals, f"Week {WEEK_NUMBER} Post-Tribal")
    create_folder(client, tribal_folder, f"Week {WEEK_NUMBER} Votes")
    create_folder(client, tribal_folder, f"Week {WEEK_NUMBER} Photographs")
    create_folder(client, tribal_folder, f"Week {WEEK_NUMBER} Miscellaneous")


def main():
    with open(".DEVTOKEN", "r") as file:
        token = file.read().strip()
    auth = box.BoxDeveloperTokenAuth(token=token)
    client = box.BoxClient(auth=auth)


    root_folder = create_folder(client, box.CreateFolderParent(id=FOLDER_ID), f"Week {WEEK_NUMBER} ({START_DATE} - {END_DATE})")
    player_self_uploads = create_folder(client, root_folder, "Player Self Uploads")
    create_player_folders(client, player_self_uploads)
    create_challenge_folders(client, root_folder)
    create_tribal_folders(client, root_folder)
    create_folder(client, root_folder, "Dream Team")
    create_folder(client, root_folder, "Misc")


if __name__ == '__main__':
    main()